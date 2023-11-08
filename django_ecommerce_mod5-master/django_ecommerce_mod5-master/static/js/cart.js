var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}

// ==================

var updateBtns2 = document.getElementsByClassName('update-cart2');

for (var i = 0; i < updateBtns2.length; i++) {
    updateBtns2[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);
        console.log('USER:', user);

        if (user == 'AnonymousUser'){
            addCookieItem2(productId, action); // Use the appropriate function for cart2
        } else {
            updateUserOrder2(productId, action); // Use the appropriate function for cart2
        }
    });
}

function updateUserOrder2(productId, action){
    console.log('User is authenticated, sending data...');

    var url = '/update_item2/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }, 
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        location.reload();
    });
}

function addCookieItem2(productId, action){
    console.log('User is not authenticated');

    if (action == 'add'){
        if (cart2[productId] == undefined){
            cart2[productId] = {'quantity': 1};
        } else {
            cart2[productId]['quantity'] += 1;
        }
    }

    if (action == 'remove'){
        cart2[productId]['quantity'] -= 1;

        if (cart2[productId]['quantity'] <= 0){
            console.log('Item should be deleted');
            delete cart2[productId];
        }
    }
    console.log('CART2:', cart2); // Use the appropriate variable for cart2
    document.cookie ='cart2=' + JSON.stringify(cart2) + ";domain=;path=/";
    
    location.reload();
}
