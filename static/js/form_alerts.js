$(document).ready(function(){
    var init_facility = $('#id_facility').val()
    $('#id_facility').change(function(){
        if ($(this).val() == init_facility) {
            $(this).css({"border-color": "#5D6B2C", "color": "black"});
            $("#facility_alert").remove();
        }
        else {
            $(this).css({"border-color": "#C88804", "color": "#C88804"})
            if (!$("#facility_alert").length) {
                $(this).after(
                '<div class="alert mt-2 mb-0 alert-warning alert-trim" id="facility_alert" role="alert">Перемещение в другое сооружение приведет к разрыву текущих коммутаций</div>' );
            };
        }
    });
});