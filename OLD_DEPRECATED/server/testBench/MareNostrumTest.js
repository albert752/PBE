const querystring = require('querystring');
var MongoClient = require('mongodb').MongoClient;

var url = "mongodb://localhost:27017/";


function query_db(collection, query, limited){
    MongoClient.connect(url, { useNewUrlParser: true }, query, function(err, db) {
        if (err) throw err;
        var database = db.db("suparurdinado");

        test = database.collection(collection).find({$and:query},{_id: 0, uid: 0}).limit(limited).toArray( function(err, result) {
            if (err) throw err;
            test=result;

            console.log(result);

            db.close();
        });
    });
}

var path = 'Timetables?day=Dimarts&limit=2&uid=8BBBF395';
var query=path.split('?'); //path.slice(0, path.indexOf('?'));

var parsed_query=[];
var limited=0
var list_criteria=query[1].split('&');
//console.log(list_criteria);
for (i=0; i<list_criteria.length; i++){
    if(list_criteria[i].includes("limit")){
	limited=parseInt(list_criteria[i].slice(6));
	//console.log(list_criteria[i].slice(6));
	//console.log(limited, list_criteria);
    }
    else if (list_criteria[i].indexOf('[') != -1){

        var end_of_comparator_index=list_criteria[i].indexOf(']');
        var criteria = list_criteria[i].slice(0, list_criteria[i].indexOf('['));
        var comparator=list_criteria[i].slice(list_criteria[i].indexOf('[')+1, end_of_comparator_index);
//        console.log(comparator);

        var query_string=list_criteria[i].replace(list_criteria[i].substring(list_criteria[i].indexOf('['),end_of_comparator_index+1), '');

        //console.log(gg[i], j, criteria, comparator, b);

        parsed_query.push(querystring.parse(query_string));
//        console.log(parsed_query)

        if ('mark' in parsed_query[i]){
            parsed_query[i]['mark']=parseInt(parsed_query[i]['mark']);
        }
//        console.log(parsed_query);
        var dict={}
        dict['$'+comparator]=parsed_query[i][criteria];
        parsed_query[i][criteria]=dict
//        console.log(parsed_query);
    }
    else{
        parsed_query.push(querystring.parse(list_criteria[i]));
    }
}
query_db(query[0], parsed_query, limited);
//console.log(query[1]);

//var parsed_query = querystring.parse(query[1]);
//console.log(parsed_query);


//var query1 = [{"mark": 8, subject: "DSBM"},{ mark:{"$lte":9.25}}];



// while(test == undefined){}

