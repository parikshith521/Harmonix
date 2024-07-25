
import config from './config.js'

function updateDOM(divName, data, song) {
	let parent_div = document.getElementById(divName);

	let song_name_node = document.createElement('p');
	let song_name_attribute_node = document.createAttribute('class');
	let song_name_text_node = document.createTextNode(song[0]);
	song_name_attribute_node.value = 'song_name';
	song_name_node.appendChild(song_name_text_node);
	song_name_node.setAttributeNode(song_name_attribute_node);

	let artist_name_node = document.createElement('p');
	let artist_name_attribute_node = document.createAttribute('class');
	let artist_name_text_node = document.createTextNode("By " + song[1]);
	artist_name_attribute_node.value = "song_artist";
	artist_name_node.appendChild(artist_name_text_node);
	artist_name_node.setAttributeNode(artist_name_attribute_node);

	let songlink = document.getElementById("songlink");
	songlink.href = song[2];

	let img_node = document.createElement('img');
	let img_class = document.createAttribute('class');
	let img_src = document.createAttribute('src');
	img_class.value = 'song_cover';
	img_src.value = song[3];
	img_node.setAttributeNode(img_class);
	img_node.setAttributeNode(img_src);


	let container_node = document.createElement('div');
	let container_class = document.createAttribute('class');
	container_class.value = 'container';
	container_node.setAttributeNode(container_class);

	songlink.addEventListener('click',(e)=>{
	e.preventDefault();
	chrome.tabs.create({url:song[2], active: true});
	});

	container_node.appendChild(song_name_node);
	container_node.appendChild(artist_name_node);
	parent_div.appendChild(container_node);
	parent_div.appendChild(img_node);
}

function getHistory(divName) {
  const microseconds_per_day = 1000 * 60 * 60 * 24;
  const oneDayAgo = new Date().getTime() - microseconds_per_day;

  let url_list = [];
  chrome.history.search(
    {
      text: "",
      startTime: oneDayAgo, 
    },
    function (history_items) {
     
      for (let i = 0; i < history_items.length; ++i) {
        const url = history_items[i].url;
        url_list.push(url);
      }
      getSong(url_list);

    }
  );

  const getSong = (url_list) => {
    let data = [];

    if(url_list.length >= 6) 
    	data = url_list.slice(0,5);
    else 
		data = url_list.slice(0,url_list.length);

    let song = [" "," "," ", " "];

	const api_url = config.API_URL + ':' + config.PORT;

    fetch(api_url , {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)

    }).then(response=>response.json())
      .then(res=>updateDOM(divName, data, res))
      .catch(error=>console.log(error));
  };
}

document.addEventListener("DOMContentLoaded", function () {
	getHistory("recommendation");
});


