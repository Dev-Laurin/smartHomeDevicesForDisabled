const frisby = require('frisby'); 

it('should be a teapot', function(){
	return frisby.post('http://127.0.0.1:5000/createDevice', {
		name: 'Alexa', description: 'something', price: 300.00, 
		recurring_price: '0.00', payment_occurence: "Once", category: "Touch", 
		homeCat: "Door", narrative: 'good', rating: 3.45, 
		link: 'www.google.com'
	}).expect('status', 200); 
}); 