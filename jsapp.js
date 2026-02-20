var language = {
	"placeholderFirst":
	{
		"ru" : "",
		"kh" : ""
	},
	"placeholderSecond":
	{
		"ru" : "",
		"kh" : ""
	}
}
let fullWindowHeight = window.innerHeight;
function convertByteArrayToAudio(byteArray) {
  // Создаем AudioContext
  const audioContext = new AudioContext();

  // Декодируем байты WAV в аудио буфер
  audioContext.decodeAudioData(byteArray.buffer, (buffer) => {
    // Создаем новый AudioBufferSourceNode
    const source = audioContext.createBufferSource();
    
    // Подключаем аудио буфер к AudioBufferSourceNode
    source.buffer = buffer;

    // Подключаем AudioBufferSourceNode к аудио выходу (воспроизведение)
    source.connect(audioContext.destination);

    // Воспроизводим аудио
    source.start();
  });
}
function getTranslate(){
		let trTo = $('.tr-to').map( (i,el) => $(el).attr('data-lg') ).get().join('-');
		let text = $('#first').val();
		$.ajax({
			type: 'POST',
			url: location.href,
			data: {
			  type:trTo,
			  text:text
			},
			success: function(data){
				console.log(data);
				//data = data.replaceAll("'",'"');
				//console.log(data);
				//var json = JSON.parse(data);
				//console.log(data);
				$('.examples .text').html('');
				$('.dictionary .text').html('');
				$('#second').val(data['main_word']);
				if(data['speech'] && location.href.includes('test')){
				
				    var src = URL.createObjectURL(new Blob([data['speech']], {type: 'audio/wav'}));
				    $('body').append('<audio controls><source src="'+src+'" type="audio/mp3" >Ваш браузер не поддерживает тег audio</audio>')

				}
				// let examples = json['main_example'];
				// let other = json['other'];
				// for (var i = 0; i < examples.split(';').length;i++){
				// 	$('.examples .text').html($('.examples .text').html()+examples.split(';')[i]+'<br>');
				// }
				// for (var i = 0; i < other.length;i++){
				// 	$('.dictionary .text').html($('.dictionary .text').html()+other[i][1]+'<br>');
				// }

				
			}
		})
		//
	}
function playWav(data) {
  const audioContext = new (window.AudioContext || window.webkitAudioContext)();
  audioContext.decodeAudioData(data, (audioBuffer) => {
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start();
  });
}


$(document).ready(function(){


	var detect = new MobileDetect(window.navigator.userAgent);
	function counterControler(){
		$('.counter').html($('textarea').eq(0).val().length+'/300');
		if ($('textarea').eq(0).val().length==0){
			$('.counter').html('');
		}
	}

	


	var scrollHeight;
	var inputTimer;
	$('textarea').css('height',($('textarea')[0].scrollHeight) + 'px;');
	$('textarea').css('overflow-y','hidden');

	$(document).on('input','textarea',function(){
		counterControler();
		if($('textarea').eq(0).val()!=""){
			$('.clear').fadeIn();
			$('.copy').fadeIn();
		}else{
			$('.clear').fadeOut();
			$('.copy').fadeOut();
		}
		clearTimeout(inputTimer);
		$('textarea').css('height','auto');
		$('textarea').css('height',(this.scrollHeight) + 'px');
		inputTimer = setTimeout(function(){
			getTranslate()
		},1000);
		if ($(this).val().length > 300) {
			$(this).val($(this).val().substring(0, 300));
			counterControler();
		}
	});

	$(document).on('click','.swap',function(){
		let f = $('.tr-to').eq(0).html();
		let fl = $('.tr-to').eq(0).attr('data-lg');
		let s = $('.tr-to').eq(1).html();
		let sl = $('.tr-to').eq(1).attr('data-lg');
		let fv = $('#first').val();
		let sv = $('#second').val();
		$('.tr-to').eq(0).html(s);
		$('.tr-to').eq(0).attr('data-lg',sl);
		$('.tr-to').eq(1).html(f);
		$('.tr-to').eq(1).attr('data-lg',fl);
		$('#first').val(sv);
		$('#second').val(fv);
		if (!detect.mobile()){
			if ($('.tr-to').eq(0).attr('data-lg')=='kh'){
				$('.keyboard').fadeIn();
			}else{
				$('.keyboard').fadeOut();
			}
		}else{
			if ($('.tr-to').eq(0).attr('data-lg')=='kh'){
			}else{
				$('.mobile_keyboard').fadeOut();
			}
		}
		counterControler();
		$('#first').attr("placeholder",language['placeholderFirst'][$('.tr-to').eq(0).attr('data-lg')]);
		$('#second').attr("placeholder",language['placeholderSecond'][$('.tr-to').eq(0).attr('data-lg')]);
	});

	$(document).on('click','.clear',function(){
		$('#first').val('');
		$('#second').val('');
		$('.clear').fadeOut();
		$('.copy').fadeOut();
		$('.counter').html('');
		counterControler();
	});

	$(document).on('click','.copy', function(){
		navigator.clipboard.writeText($('#second').val());
	});

	$(document).on('click','.char',function(){
		clearTimeout(inputTimer);
		$('#first').val($('#first').val()+$(this).html());
		$('#first').focus();
		counterControler();
		inputTimer = setTimeout(function(){
			getTranslate()
		},1000);
	});

	$(document).on('focus','#first',function(){
		if (detect.mobile() && $('.tr-to').eq(0).attr('data-lg')=='kh'){
			$('.mobile_keyboard').fadeIn();
		}
	});

	$(document).on('click','.close',function(){
		$('.mobile_keyboard').fadeOut();
		$('textarea').blur();
	})

});