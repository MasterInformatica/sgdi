/*******************************************************************************
Autores: Luis M. Costero Valero & Jesús Doménech Arellano
Grupo 04

Este código es fruto ÚNICAMENTE del trabajo de sus miembros. Declaramos no 
haber colaborado de ninguna manera con otros grupos, haber compartido el ćodigo 
con otros ni haberlo obtenido de una fuente externa.
*******************************************************************************/


/*******************************************************************************
**************************** AGGREGATION FRAMEWORK *****************************
*******************************************************************************/

// Listado de pais-numero de usuarios ordenado de mayor a menor por numero de 
// usuarios.
function agg1(){
  var pipeline = [
    {$group :{ _id:"$country",num_user:{$sum:1}}},
    {$sort:{"num_user":-1}}
  ];
  return db.agg.aggregate(pipeline);
}


// Listado de pais-numero total de posts de los 3 paises con mayor numero total 
// de posts, ordenado de mayor a menor por numero de posts.
function agg2(){
  var pipeline = [
    {$group :{ _id:"$country",num_post:{$sum:"$num_posts"}}},
    {$sort:{"num_post":-1}},
    {$limit: 3}
  ];
  return db.agg.aggregate(pipeline);
}

  
// Listado de aficion-numero de usuarios ordenado de mayor a menor numero de 
// usuarios.
function agg3(){
  var pipeline = [
    {$unwind : {path:"$likes"}},
    {$group: { _id:"$likes",num_user:{$sum:1}}},
    {$sort:{"num_user":-1}}
  ];
  return db.agg.aggregate(pipeline);
}  
  
  
// Listado de aficion-numero de usuarios restringido a usuarios espanoles y
// ordenado de mayor a menor numero de usuarios.
function agg4(){
  var pipeline = [
    {$match: { country: "Spain"}},
    {$unwind : {path:"$likes"}},
    {$group: { _id:"$likes",num_user:{$sum:1}}},
    {$sort:{"num_user":-1}}
  ];
  return db.agg.aggregate(pipeline);
}



/*******************************************************************************
********************************** MAPREDUCE ***********************************
*******************************************************************************/
  
// Listado de aficion-numero de usuarios restringido a usuarios espanoles.
function mr1(){
	return db.agg.mapReduce(
	  function(){
	    for (v in this.likes) {
	      emit(this.likes[v],1);
	    }
	  },
	  function(key,values){
	    return Array.sum(values);
	  },
	  {
	    query : { country: "Spain"},
	    out : {inline: 1}
	  }).results;
}


// Listado de numero de aficiones-numero de usuarios, es decir, cuAntos
// usuarios tienen 0 aficiones, cuantos una aficion, cuantos dos aficiones, etc.
function mr2(){
	return db.agg.mapReduce(
	  function(){
	    if(!this.likes)
	      emit(0,1);
	    else
	      emit(this.likes.length,1);
	  },
	  function(key,values){
	    return Array.sum(values);
	  },
	  {
	    out : {inline: 1}
	  });
}


// Listado de pais-numero de usuarios que tienen mas posts que contestaciones.
function mr3(){
	return db.agg.mapReduce(
	  function(){
	    if (this.num_posts > this.num_answers)
	      emit(this.country,1);
	  },
	  function(key,values){
	    return Array.sum(values);
	  },
	  {
//	    query: {"num_posts": {$gt: "num_answers"}},
	    out : {inline: 1}
	  });

}


// Listado de pais-media de posts por usuario.
function mr4(){
	return db.agg.mapReduce(
	  function(){
	      emit(this.country,this.num_posts);
	  },
	  function(key,values){
	    return Array.sum(values)/values.length;
	  },
	  {
	    out : "total"
	  }).find();
}




