var express = require('express');
var app = express();

var AWS = require('aws-sdk');
var uuid4 = require('uuid/v4');
var cors = require('cors');
var fs = require('fs');
const bodyParser = require('body-parser');
const fileUpload = require('express-fileupload');

var bigScore = 0

var accessKeyId = 'AKIAIYY4M5SFDFKW4H7A';
var secretAccessKey = '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';
AWS.config.region = 'us-west-2';
AWS.config.update({
	accessKeyId: accessKeyId,
	secretAccessKey: secretAccessKey
});
var s3 = new AWS.S3();
var s3bucket = new AWS.S3({params:{Bucket:'addax'}});

//Satori requirements + configuration
var RTM = require("satori-rtm-sdk");
var endpoint = "wss://jn46sxsj.api.satori.com";
var appkey = "ABda3cfaC4331cc76e9bBA186FB8328E";
var channelName = "views";
var client = new RTM(endpoint, appkey);
//Satori client events
client.on("enter-connected", function () {
  console.log("Connected to Satori RTM!");
});
client.on("leave-connected", function () {
  console.log("Disconnected from Satori RTM");
});
client.on("error", function (error) {
  var reason;
  if (error.body) {
    reason = error.body.error + " - " + error.body.reason;
  } else {
    reason = "unknown reason";
  }
  console.log("RTM client failed: " + reason);
});
client.start();



app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());
app.use(cors());
app.use(fileUpload());


app.post('/upload',function(req,res){
	info = req.files.info
	video = req.files.video

	var uuid = uuid4();

	infoData = info.data.toString()
	var score =  Math.random() * (10 - 0);
	var views = Math.random() * (20-0);
	infoData = infoData.replace(/.$/,'');
	infoData= infoData + ',"link": "https://s3-us-west-2.amazonaws.com/addax/all/' + uuid + '/video.mp4","uuid": "' + uuid + '","views":' + views + '}'


	console.log(infoData)
	var infoName = "all/" + uuid + "/info.json"
	var infoOptions = {
        Key: infoName,
        Body: infoData,
        ACL: "public-read",
        ContentType: "application/json"
   }


   var videoName = "all/" + uuid + "/video.mp4"
   var videoOptions = {
        Key: videoName,
        Body: video.data,
        ACL: "public-read",
        ContentType: "video/mp4"
   }

    s3bucket.putObject(infoOptions,function (err, data) {
    	s3bucket.putObject(videoOptions,function(err,data){
    		res.send(err)
    	})
	});



});

app.post("/uploadFile",function(req,res){
	//console.log("asd;kljfdkls;jfdkls;")
	//var video = req.files.video
	//console.log(req.files)
	//var companyName = req.body.companyName
	//var adName = req.body.adName

	//var uuid = uuid4()
	var score =  Math.random() * (10 - 0);
	//infoData = '{"view_count": 22458, "impact_score":' +  score + ', "title": "' + adName + '", "dislike_count": 1, "like_count": 25, "uploader": "' + companyName + '", "duration": 15, "thumbnail": "https://i.ytimg.com/vi/vqnPHO1ruBs/maxresdefault.jpg","link": "https://s3-us-west-2.amazonaws.com/addax/all/02a4cb6c-da21-47f5-b3f7-7c49fa0a8c2d/video.mp4","uuid": "02a4cb6c-da21-47f5-b3f7-7c49fa0a8c2d","views":1.7382402199457214}'
	bigScore = score
	console.log(bigScore)
	res.send(200)
	/*console.log(bigScore)
	var infoName = "all/" + uuid + "/info.json"
	var infoOptions = {
        Key: infoName,
        Body: infoData,
        ACL: "public-read",
        ContentType: "application/json"
   }


   var videoName = "all/" + uuid + "/video.mp4"
   var videoOptions = {
        Key: videoName,
        Body: video.data,
        ACL: "public-read",
        ContentType: "video/mp4"
   }


    s3bucket.putObject(infoOptions,function (err, data) {
    	s3bucket.putObject(videoOptions,function(err,data){
    		res.send(200)
    	})
	});*/

});

app.get("/score",function(req,res){
	console.log("ASDF" + bigScore)
	object= {
		"score":bigScore
	}
	res.send(object)

});





app.get('/topTen',function(req,res){
	var params = {
		Bucket: "addax",
		Key: "topTen.json"
	};

	s3.getObject(params,function(err,data){
		if (err){
			console.log(err, err.stack); // an error occurred
		}else{
			console.log(data.Body.toString())
			data = data.Body.toString()
			res.send(data)
		}
	});
});

app.get('/all', function (req, res) {

	var params = {
		Bucket: "addax",
		Delimiter: '/',
		Prefix:'all/'

	};

	var commonPrefixes = []
	var info = []
	s3.listObjects(params, function(err, data) {
		if (err){
			console.log(err, err.stack); // an error occurred
		}else{
			commonPrefixes = data.CommonPrefixes;
			//console.log(commonPrefixes)
			commonPrefixes = commonPrefixes.map(function(prefix){
				return prefix.Prefix;
			});
			var itemsProcessed = 0;
			commonPrefixes.forEach(function(key){

				Key = key + "info.json"
				var params = {
					Bucket: "addax",
					Key: Key
				};

				s3.getObject(params, function(err, data) {
					if (err){
						console.log(err, err.stack); // an error occurred
					}else{

					console.log(data)
					info.push(JSON.parse(data.Body.toString()))
					itemsProcessed++
					if(itemsProcessed===commonPrefixes.length){
						res.send(info)
					}


					}
				});

			});




		}


	});




});

//increment view count
app.post('/view',function(req, res){
  var client_uuid = req.body.uuid;
  var name = "all/"+client_uuid+"/info.json";
	
  s3bucket.getObject({Key:name},function(err, data){
    if(err){
      console.log("ERROR MSG: " + err);
      res.sendStatus(500).send(err);
    }
    else{
      var object = JSON.parse(data.Body.toString());
      object.views = parseInt(object.views)+1;
      var new_json = JSON.stringify(object);

      s3bucket.upload({
        Key:name,
        Body: new_json,
        ACL: "public-read",
        ContentType: "application/json"
      },function(err,data){
        if(err){
          console.log("ERROR MSG: "+err);
        }
        else{
          if(client.isConnected()){
            var view_data = {
              uuid: client_uuid,
              view_count: object.views
            }

            client.publish(channelName, view_data, function(pdu) {
              if (pdu.action.endsWith("/ok")) {
                // Publish is confirmed by Satori RTM.
                console.log("Data is published");
                //console.log(JSON.stringify(data));
              } else {
                console.log("Publish request failed: " + pdu.body.error + " - " + pdu.body.reason);
              }
            });
          }
        }
      });
      res.send(JSON.stringify(object.views));
    }
  });
});




app.listen( process.env.PORT || 3000);
