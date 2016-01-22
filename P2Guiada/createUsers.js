function createUsers(n){
	var comp = ["Microsoft","Google","Amazon","IBM"];
	var letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
	for (var i = 0; i < n; ++i){
  	var p = {};
 		p.company = comp[Math.floor(Math.random() * comp.length)];
  	p.username = "";
  	for( var j=0; j < 5; j++ ){
    	p.username += letras.charAt(Math.floor(Math.random() * letras.length));
	  }
  	p._id = i;
  	p.year = 1900 + Math.floor(Math.random() * 115);
	  db.users.insert(p);
	}
}
