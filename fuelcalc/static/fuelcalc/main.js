$(document).ready( function() {

	$("#id_start_zip").change( function() {
		var start_zip = $(this).val();
		$.ajax({
			url: '/ajax/validate_start_zip',
			data: {
				'start_zip': start_zip
			},
			dataType: 'json',
			success: function(data) {
				if(data.is_invalid == true)
					$("#error-id_start_zip").html("Invalid Start Zip Code");
				else
					$("#error-id_start_zip").html("");
			}

		});
	});
	$("#id_dest_zip").change( function() {
		var dest_zip = $(this).val();
		$.ajax({
			url: '/ajax/validate_dest_zip',
			data: {
				'dest_zip': dest_zip
			},
			dataType: 'json',
			success: function(data) {
				if(data.is_invalid == true)
					$("#error-id_dest_zip").html("Invalid Dest Zip Code");
				else
					$("#error-id_dest_zip").html("");
			}

		});
	});

	$("#id_year").change( function() {
		var year = $(this).val();
		$.ajax({
			url: '/ajax/year_processing',
			data: {
				'year': year
			},
			dataType: 'json',
			success: function(data) {
				if(data.is_invalid == true) {
					$("#error-id_year").html("Invalid Year. Year must be between 1985 and 2017");
					$("#id_make").html("");
					$("#id_model").html("");
				}

				else {
					$("#error-id_year").html("");
					$("#id_make").html("");
					for(var i = 0; i < data.makes.length; i++) {
						 $("#id_make").append("<option>" + data.makes[i] + "</option>");
					 }
				 }
			}
		});
	});

	$("#id_make").change( function() {
		var year = $("#id_year").val();
		var make = $(this).val();
		$.ajax({
			url: '/ajax/get_models',
			data: {
				'year': year,
				'make': make,
			},
			dataType: 'json',
			success: function(data) {
				$("#id_model").html(" ");
				for(var i = 0; i < data.models.length; i++) {
					 $("#id_model").append("<option>" + data.models[i] + "</option>");
				}
			}
		});
	});

	$(".split").click(function() {
		var totalCost = parseFloat($("#cost").text().substr(1));
        if (this.id == 'b1') {
			$("#costPerPerson").html("$" + totalCost.toFixed(2));
			$(this).addClass('active').siblings().removeClass('active');
        }
        else if (this.id == 'b2') {
            $("#costPerPerson").html("$" + (totalCost/2.0).toFixed(2));
			$(this).addClass('active').siblings().removeClass('active');
        }
		else if (this.id == 'b3') {
            $("#costPerPerson").html("$" + (totalCost/3.0).toFixed(2));
			$(this).addClass('active').siblings().removeClass('active');
        }
		else if (this.id == 'b4') {
            $("#costPerPerson").html("$" + (totalCost/4.0).toFixed(2));
			$(this).addClass('active').siblings().removeClass('active');
        }
		else if (this.id == 'b5') {
            $("#costPerPerson").html("$" + (totalCost/5.0).toFixed(2));
			$(this).addClass('active').siblings().removeClass('active');
        }
		changeVenmoAmtVal($("#costPerPerson").html());
    });


})

function changeVenmoAmtVal(value) {
	$("#amount").val(value);
}
