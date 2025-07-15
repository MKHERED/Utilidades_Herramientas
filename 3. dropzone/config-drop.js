/*jQuery(document).ready(function($){
        Dropzone.options.myDrop = {
            uploadMultiple: true,
            maxFileSize: 22,
            init: function init() {
                this.on('error', function(){
                    alert('Error al subir archivo');
                })
            },
            accept: function(file, done) {
                if (file.name == "*.xlsx") {
                  done("Es un excel");
                }
                else { done(); }
              }
        }
})*/