$(document).ready(function(){
    $('#brand-filter li').click(function(){
        var brand = $(this).data('brand');
        $('.title').html(brand);
        $('#cat-filter li').each(function() {
           $(this).hide();
           var cat = $(this).data('cat');
           if (brand==cat){
               $(this).html(cat);
               $(this).show();
            };
        })
    });
});

