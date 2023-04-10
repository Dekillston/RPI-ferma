console.log('General.js on');
// AJAX
function Ajax(INF, FUN) {
	
	$.ajax({
		url:'',
		type: 'get',
		contentType: 'application/json',
		data: INF,
		success: FUN
	});
}
window.onload = () => {
// Кнопка вызова
function ButtonEnter() {
	document.addEventListener("click", function(e) {
		var block = e.target;
		for(var n = 1; true; n++) {
			var button = document.getElementById('RELE'+n);
			if(button == null) {
				break;
			}
			if(block == button) {
				Ajax({ReleButton:block.getAttribute('id')}, (data) => {
					block.textContent = data.ReleButton;
					
				});
			}
			
		}
	});
}
ButtonEnter();
// Функция обновления Данных
var Second = 0;
var DataUpdate = {};
function IntervalData() {
	var Time = 30;
	if(Second == 0) {
		DataUpdate = {Temperature:'TEM_DHT22', Humidity: 'HUM_DHT22'};
	} else {
		DataUpdate = {ReleData:'NUR_RELE', Water: 'WAR_DAT'};
	}
	Ajax(DataUpdate, (data) => {
		if(data.Temperature !== null) {
			document.getElementById('Temperature').textContent = data.Temperature;
			document.getElementById('Humidity').textContent = data.Humidity;
			return;
		}
		IntervalRele(data.ReleData);
		IntervalWater(data.Water);
	});
	if(Second >= Time) {Second = 0;} else {Second++;}
}
IntervalData();
setInterval(IntervalData, 1000)
// Функция для обновления реле
function IntervalRele(data) {
	for(var n = 1; true; n++) {
		var button = document.getElementById('RELE'+n);
		if(button == null) {
			break;
			
		}
		if(data[n-1] == 1) {
			button.textContent = 'ON';
		} else if (data[n-1] == 0) {
			button.textContent = 'OFF';
		}
	}	
}
// Функция датчика воды
function IntervalWater(data) {
	for(var n = 1; true; n++) {
		var block = document.getElementById('Water_'+n);
		if(block == null) {
			break;	
		}
		if(data[n-1] == 0) {
			block.textContent = 'Заполнен';
		} else if (data[n-1] == 1) {
			block.textContent = 'Пустой';
		}
	}
}
}



