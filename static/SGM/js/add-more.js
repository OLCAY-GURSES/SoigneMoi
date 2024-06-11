

(function($) {
    "use strict";


	// Specialization Add More

    $(".specialization-info").on('click','.trash', function () {
		$(this).closest('.specialization-cont').remove();
		return false;
    });

    $(".add-specialization").on('click', function () {

        var specializationcontent = '<div class="row form-row specialization-cont">' +
			'<div class="col-12 col-md-10 col-lg-5">' +
				'<div class="form-group">' +

					'<label>Nouvelle spécialité</label>' +

					'<input type="text" name="specialization" class="form-control">' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2 col-lg-2">' +
				'<label class="d-md-block d-sm-none d-none">&nbsp;</label>' +
				'<a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a>' +
			'</div>' +
		'</div>';

        $(".specialization-info").append(specializationcontent);
        return false;
    });



})(jQuery);