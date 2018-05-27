$(document).ready(function() {
    $('#cal-result').on('click',function(event) {
        calcualtebmi()
    });

    $('.weight').on('click',function(event) {
        var id = $(this).attr('id');
        $('.weight').removeClass('selected-weight');
        $(this).addClass('selected-weight');
        $(".weight").removeClass("active-weight");
        $(this).addClass("active-weight");
        $('#weight-measure').val(id);
        calcualtebmi()
    });
    $('.height').on('click',function(event) {
        var id = $(this).attr('id');
        $('.height').removeClass('selected-height');
        $(this).addClass('selected-height');
        $(".height").removeClass("active-height");
        $(this).addClass("active-height");
        $('#height-measure').val(id);
        calcualtebmi()
    });
});

function calcualtebmi(){

    var weight = $('#weight-value').val();
    var height_ft = $('#height-value-ft').val();
    var height_in = $('#height-value-in').val(); 
    var height = $('#height-value').val();
    if((weight != 0 && height != 0) || (weight != 0 && height_ft != 0 && height_in != 0) ){

        if($('#weight-measure').val() == "lbs"){
            weight = weight * 0.453592;
        }
        if ($('#height-measure').val() == "cm") {
            height = height / 100;
        }else{
            height_in = +height_in + +(height_ft * 12);
            height = height_in * 0.0254;
        }
        var bmi = weight/(height*height);

        switch (true) {
            case (bmi > 0 && bmi <= 18):
                $("#bmi-result").val(parseFloat(bmi).toFixed(2));
                $('#cal-result').removeClass('hty-bmi ow-bmi ob-bmi eob-bmi');
                $('#cal-result').addClass('uw-bmi');
                $('#cal-result').html('Underweight');
                break;
            case (bmi > 18 && bmi < 25):
                $("#bmi-result").val(parseFloat(bmi).toFixed(2));
                $('#cal-result').removeClass('uw-bmi ow-bmi ob-bmi eob-bmi');
                $('#cal-result').addClass('hty-bmi');
                $('#cal-result').html('Healthy');
                break;
            case (bmi >= 25 && bmi < 30):
                $("#bmi-result").val(parseFloat(bmi).toFixed(2));
                $('#cal-result').removeClass('hty-bmi uw-bmi ob-bmi eob-bmi');
                $('#cal-result').addClass('ow-bmi');
                $('#cal-result').html('Overweight');
                break;
            case (bmi >= 30 && bmi < 40):
                $("#bmi-result").val(parseFloat(bmi).toFixed(2));
                $('#cal-result').removeClass('hty-bmi ow-bmi uw-bmi eob-bmi');
                $('#cal-result').addClass('ob-bmi');
                $('#cal-result').html('Obese');
                break;
            case (bmi >=40):
                $("#bmi-result").val(parseFloat(bmi).toFixed(2));
                $('#cal-result').removeClass('hty-bmi ow-bmi ob-bmi uw-bmi');
                $('#cal-result').addClass('eob-bmi');
                $('#cal-result').html('Extremly Obese');
                break;
            default:
                $("#bmi-result").val("(**__**)_*)");
                $('#cal-result').removeClass('hty-bmi ow-bmi ob-bmi uw-bmi eob-bmi');
                $('#cal-result').addClass('btn-warning');
                $('#cal-result').html('Unable to Calculate');
                break;
        }    
    }   
    
}