var updateBtns=document.getElementsByClassName('update-carrito')

for (var i = 0; i < updateBtns.length; i++){
	updateBtns[i].addEventListener('click', function(){
		var productosId = this.dataset.productos
		var action = this.dataset.action
		console.log('productosId:', productosId,'action:',action)

		console.log('USER:', user)
		if(user == 'AnonymousUser'){
			addCookieItem(productosId, action)
		}else{ 
			updatePedido(productosId, action)
			
		}
	})

}

function addCookieItem(productosId,action){
	console.log('no logueado')
	if (action == 'add'){
		if (cart[productosId] == undefined){
			cart[productosId] = {'quantity':1}
		}
		else{
			cart[productosId]['quantity'] += 1
		}
	}

	if (action == 'remover'){
		cart[productosId]['quantity'] -= 1
		if (cart[productosId]['quantity'] <= 0){
			console.log('Articulo elminado')
			delete cart[productosId]
	
		}
	}
	console.log('Cart',cart)
	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload()
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
			return response.json()
		})

		.then((data)=>{
			console.log('data:', data)
			location.reload()
		})
	}