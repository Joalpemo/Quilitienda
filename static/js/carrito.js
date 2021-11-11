var updateBtns=document.getElementsByClassName('update-carrito')

for (var i=0; i<updateBtns.length;i++){
	updateBtns[i].addEventListener('click',function(){
		var productosId = this.dataset.productos
		var action = this.dataset.action
		console.log('productosId:', productosId,'action:',action)

		console.log('USER:',user)
		if(user=='AnonymousUser'){
			console.log('No esta logueado')
		}else{
			updatePedido(productosId,action)
		}
	})

}

function updatePedido(productosId,action){
		console.log('enviado data')

		var url = '/Agregar/'

		fetch(url,{
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'productosId': productosId,'action':action})
		})
		.then((response)=>{
			return response.json();
		})
		.then((data)=>{
			console.log('data:', data)
		});
	}