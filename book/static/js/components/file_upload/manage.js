  $(document).ready(function(){

    console.log('NAG WORK ANG FILE UPLOAD AMEN');

    $('.custom-file-input').on('change', function(){
      var fileName = $(this).val().split('\\').pop();
      $(this).next('.custom-file-label').html(fileName);
    });

  });