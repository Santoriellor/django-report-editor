// ********************************** Javascript to disabled the first otpion of the client select
// ********************************** and disabled the motor select when necessary
// Check if the element exists
if ($('#id_client').length > 0) {
    // Element exists
    $(document).ready(function() {
        var selectClientElement = $('#id_client');
        var firstClientOption = selectClientElement.find('option:first');
        var testClient = selectClientElement.val();
        if (testClient == '') {
            $('#id_motor_serial_number').prop('disabled', true);
        }
        firstClientOption.hide();
    });
};

// ********************************Javascript to update the 'motor' select in the 'ReportForm' form
$(document).ready(function() {
    function updateClientSelect () {
        var clientId = $(this).val();
        if (!clientId) {
            $('#id_sparkplug').val(null).attr('placeholder', '---------');
            $('#id_oil_filter').val(null).attr('placeholder', '---------');
            $('#id_impeller').val(null).attr('placeholder', '---------');
            return; // Exit early if motorId is empty
        }
        $.ajax({
            url: '/get_motors/',  // URL to fetch motors for the selected client
            data: {
                'client_id': clientId
            },
            dataType: 'json',
            success: function(data) {
                var motorSelect = $('#id_motor_serial_number');
                var motor_serial = motorSelect.val()
                motorSelect.empty();
                if (data.motors.length === 0) {
                    // If no motors are returned, manually append the empty option
                    motorSelect.append($('<option>', {
                        value: '',
                        text: 'No motor associated'
                    }));
                } else {
                    $.each(data.motors, function(index, motor) {
                        if (motor.serial_number == motor_serial) {
                            motorSelect.append($('<option>', {
                                selected: true,
                                value: motor.serial_number,
                                text: motor.serial_number
                            }));
                        } else {
                            motorSelect.append($('<option>', {
                                value: motor.serial_number,
                                text: motor.serial_number
                            }));
                        }
                    });
                    // Change the motor select to disabled false
                    var selectMotorElement = document.getElementById('id_motor_serial_number');
                    selectMotorElement.disabled = false;
                }
                // Trigger the change event to update the motor data
                $('#id_motor_serial_number').trigger('change');
            }
        });
    };
    $('#id_client').on('change', updateClientSelect);
    $('#id_client').trigger('change');
});

// ********************************Javascript to update the fields corresponding with the selected 'motor'
// Update the motor data selects
$(document).ready(function() {
    $('#id_motor_serial_number').change(function() {
        var motorId = $(this).val();
        if (!motorId) {
            $('#id_sparkplug').val(null).attr('placeholder', 'No spark plug associated');
            $('#id_oil_filter').val(null).attr('placeholder', 'No oil filter associated');
            $('#id_impeller').val(null).attr('placeholder', 'No impeller associated');
            return; // Exit early if motorId is empty
        }
        $.ajax({
            url: '/get_motor_data/',  // URL to fetch motor data for the selected motor
            method: 'GET',  // Specify the HTTP method (GET by default)
            data: {
                'motor_serial_number': motorId
            },
            dataType: 'json',
            success: function(data) {
                var sparkplugInput = $('#id_sparkplug');
                sparkplugInput.empty();
                if (data.sparkplug) {
                    sparkplugInput.val(data.sparkplug);
                } else {
                    // If no sparkplugs are returned, manually append the empty input
                    sparkplugInput.val(null).html('No spark plug associated');
                }
                var oilfilterInput = $('#id_oil_filter');
                oilfilterInput.empty();
                if (data.oilfilter) {
                    oilfilterInput.val(data.oilfilter);
                } else {
                    // If no oilfilter are returned, manually append the empty input
                    oilfilterInput.val(null).html('No oil filter associated');
                }
                var impellerSelect = $('#id_impeller');
                impellerSelect.empty();
                if (data.impeller) {
                    impellerSelect.val(data.impeller);
                } else {
                    // If no sparkplugs are returned, manually append the empty input
                    impellerSelect.val(null).html('No impeller associated');
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.error('Error fetching motor data:', errorThrown);
                // Handle error condition if necessary
            }
        });
    });
});

// add a confirm on delete button
document.addEventListener('DOMContentLoaded', function() {
  var deleteLinks = document.querySelectorAll('.delete-link');

  deleteLinks.forEach(function(link) {
    link.addEventListener('click', function(event) {
      event.preventDefault(); // Prevent the default action (i.e., following the link)

      var confirmation = confirm('Are you sure you want to delete?');

      if (confirmation) {
        window.location.href = link.href; // Proceed with the delete action
      }
    });
  });
});
