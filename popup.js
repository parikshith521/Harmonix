



function updateDOM(divName, data, song) {
  let popupDiv = document.getElementById(divName);


  let elementNode = document.createElement('p');
  let attributeNode = document.createAttribute('class');
  let textNode = document.createTextNode(song[0]);
  attributeNode.value = 'song_name';
  elementNode.appendChild(textNode);
  elementNode.setAttributeNode(attributeNode);

  let elementNode1 = document.createElement('p');
  let attributeNode1 = document.createAttribute('class');
  let textNode1 = document.createTextNode("By " + song[1]);
  attributeNode1.value = "song_artist";
  elementNode1.appendChild(textNode1);
  elementNode1.setAttributeNode(attributeNode1);

  let songlink = document.getElementById("songlink");
  songlink.href = song[2];

  let imgNode = document.createElement('img');
  let imgClass = document.createAttribute('class');
  let imgSrc = document.createAttribute('src');
  imgClass.value = 'songcover';
  imgSrc.value = song[3];
  imgNode.setAttributeNode(imgClass);
  imgNode.setAttributeNode(imgSrc);


  let containerNode = document.createElement('div');
  let containerClass = document.createAttribute('class');
  containerClass.value = 'container';
  containerNode.setAttributeNode(containerClass);


  songlink.addEventListener('click',(e)=>{
    e.preventDefault();
    chrome.tabs.create({url:song[2], active: true});
  });

  containerNode.appendChild(elementNode);
  containerNode.appendChild(elementNode1);
  popupDiv.appendChild(containerNode);
  popupDiv.appendChild(imgNode);
}

function getHistory(divName) {
 

  const microsecondsperDay = 1000 * 60 * 60 * 24;
  const oneDayAgo = new Date().getTime() - microsecondsperDay;

  let urlList = [];

  chrome.history.search(
    {
      text: "",
      startTime: oneDayAgo, 
    },
    function (historyItems) {
     
      for (let i = 0; i < historyItems.length; ++i) {
        const url = historyItems[i].url;
        urlList.push(url);
      }
      getSong(urlToCount);

    }
  );

  const getSong = (urlList) => {

    let data = urlList.slice(0,min(5,urlToCount.length));

    let song = [" "," "," ", " "];

    fetch('http://127.0.0.1:8080/' , {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)

    }).then(response=>response.json())
      .then(res=>{
        const song = res
        updateDOM(divName, data,song);
      })
      .catch(error=>console.log(error));

    
  };
}

document.addEventListener("DOMContentLoaded", function () {
  
	getHistory("typedUrl_div");
  
});


