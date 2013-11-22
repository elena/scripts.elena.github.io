from celery.contrib.methods import task
from clickatell import constants as clickatell_constants
from clickatell.api import Clickatell
from django.conf import settings
from django.template.loader import render_to_string


class SMSMethod(object):
    template_name = 'dispatch_methods/sms_method.txt'
    test_template_name = 'dispatch_methods/sms_method_test.txt'

    def __init__(self, request=None):
        self.request = request
        self.clickatell = Clickatell(
            settings.CLICKATELL_USERNAME,
            settings.CLICKATELL_PASSWORD,
            settings.CLICKATELL_APP_ID,
            sendmsg_defaults={
                'req_feat':clickatell_constants.FEAT_NUMER,
                'sender':settings.CLICKATELL_NUMBER,
                'concat':'10',
                'escalate':'1',
                'mo':'1',
            }
        )

    def get_rendered_template(self, **kwargs):
        template_name = kwargs.get('template_name', self.template_name)

        context = {
            'request': self.request,
            'dispatch': self.request.dispatch,
            'site_group': self.request.site_group
        }
        return render_to_string(template_name, context)

    def enqueue_pre_post(self):
        pre_countdown = self.request.dispatch.get_pre_dispatch_message_countdown()
        post_countdown = self.request.dispatch.get_post_dispatch_message_countdown()

        if pre_countdown > 0:
            self.send_pre.apply_async([], countdown=pre_countdown)

        self.send_post.delay(post_countdown)

    def get_contact_numbers(self):
        people = self.request.site_group.contact_people.all()
        return [person.mobile for person in people]

    @task(name='SMSMethod.send_message')
    def send_message(self, recipients, text):
        self.clickatell.sendmsg(
            recipients=recipients,
            text=text
        )

    def send_templated_message(self, template_name):
        rendered = self.get_rendered_template(template_name=template_name)
        self.send_message.delay(self.get_contact_numbers(), rendered)

    @task(name='SMSMethod.send_pre')
    def send_pre(self):
        if self.request.site_status_display() == 'Unknown':
            # send please respond asap message
            tmpl_name = 'dispatch_methods/sms_method_pre_unknown.txt'

        elif self.request.site_status_display() == 'Accepted':
            # send reminder message
            tmpl_name = 'dispatch_methods/sms_method_pre_available.txt'

        else:
            return

        self.send_templated_message(tmpl_name)

    @task(name='SMSMethod.send_post')
    def send_post(self, delay_seconds):
        rendered = self.get_rendered_template(template_name='dispatch_methods/sms_method_post.txt')
        self.clickatell.sendmsg(
            recipients=self.get_contact_numbers(),
            deliv_time=int(delay_seconds/60)
        )

    @task(name='SMSMethod.send')
    def send(self):
        self.enqueue_pre_post()
        self.send_templated_message(self.template_name)

    @task(name='SMSMethod.send_test')
    def send_test(self):
        self.send_templated_message(self.test_template_name)
