
(function($) {
    "use strict";

	// medicine Add More
	
    $(".medicine-info").on('click','.trash', function () {
		$(this).closest('.medicine-cont').remove();
		return false;
    });

    $(".add-medicine").on('click', function () {  
		
		var medicinecontent = '<div class="row form-row medicine-cont">' +
			'<div class="col-12 col-md-10 col-lg-11">' +
				'<div class="row form-row">' +
					'<div class="col-12 col-md-6 col-lg-4">' +
						'<div class="form-group">' +
							'<label>Nom du médicament</label>' +
							'<input type="text" name="medicine_name" class="form-control">' +
						'</div>' +
					'</div>' +
					'<div class="col-12 col-md-6 col-lg-3">' +
						'<div class="form-group">' +
							'<label>Quantité</label>' +
							'<input type="text" name="quantity" class="form-control">' +
						'</div>' +
					'</div>' +
                    '<div class="col-12 col-md-6 col-lg-3">' +
						'<div class="form-group">' +
							'<label>Fréquence</label>' +
							'<input type="text" name="frequency" class="form-control">' +
						'</div>' +
					'</div>' +

					'<div class="col-12 col-md-6 col-lg-3">' +
						'<div class="form-group">' +
							'<label>Date du Début de Traitement </label>' +
							'<input type="text" name="start_day" class="form-control">' +
						'</div>' +
					'</div>' +
					'<div class="col-12 col-md-6 col-lg-3">' +
						'<div class="form-group">' +
							'<label>Date Fin de Traitement </label>' +
							'<input type="text" name="end_day" class="form-control">' +
						'</div>' +
					'</div>' +
					'<div class="col-12 col-md-6 col-lg-4">' +
						'<div class="form-group">' +
							'<label>Instruction</label>' +
							'<input type="text" name="instruction" class="form-control">' +
						'</div>' +
					'</div>' +

				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2 col-lg-1"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
        $(".medicine-info").append(medicinecontent);
        return false;
    });	
	
	
	// Test Add More

	$(".test-info").on('click','.trash', function () {
		$(this).closest('.test-cont').remove();
		return false;
	});

	$(".add-test").on('click', function () {  
		
		var testcontent = '<div class="row form-row test-cont">' +
			'<div class="col-12 col-md-10 col-lg-11">' +
				'<div class="row form-row">' +
					'<div class="col-12 col-md-5 col-lg-5">' +
						'<div class="form-group">' +
							'<label>Nom du test</label>' +
							'<input type="text" name="test_name" class="form-control">' +
						'</div>' +
					'</div>' +
					'<div class="col-12 col-md-6 col-lg-6">' +
						'<div class="form-group">' +
							'<label>Description</label>' +
							'<input type="text" name="description" class="form-control">' +
						'</div>' +
					'</div>' +
					
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2 col-lg-1"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
		$(".test-info").append(testcontent);
		return false;
	});

		
})(jQuery);