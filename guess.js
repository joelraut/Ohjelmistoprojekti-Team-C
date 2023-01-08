'use strict';

//  ile's very usable function
async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(response.statusText);
  }
  return await response.json();
}

const hello = document.createTextNode(
    'In this game you are given a sample sound in a mystery language, your job is to guess the correct European country.');
document.querySelector('#description').appendChild(hello);
// form for player name
document.querySelector('#player-form').
    addEventListener('submit', function(evt) {
      evt.preventDefault();
      const playerName = document.querySelector('#player-input').value;
      document.querySelector('#player-modal').classList.add('hide');
      document.querySelector("#sound_button").classList.remove("hide");     // makes sound button not hidden
      loop(playerName);
    });

async function loop(playerName) {
  try {
    const apiUrl = 'http://127.0.0.1:5000/';
    const user = playerName;
    const map = L.map('map', {
      minZoom: 3,
      maxZoom: 8,
    }).setView([51.505, -0.09], 3.2);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 8,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
    L.control.scale().addTo(map);
    document.querySelector("#info").classList.add("info2");


    const jsonData = await fetchJson(apiUrl + 'loop/' + user);
    const id = jsonData['id'];                                            // pelin id talteen
    let count_country = jsonData['country_num'];
    const locations = jsonData['locations'];
    const namae = jsonData['namae'];
    const country_name = jsonData['country_name'];
    const player = jsonData['player'];
    const name = document.createTextNode("Player name: " + player);
    document.querySelector("#name").appendChild(name);
    document.querySelector("#name").classList.remove("hide");

    start(id, count_country, locations, map, namae, country_name);
  } catch (error) {
    console.log(error);
  }
}

async function start(Id, count_country, locations, map, namsku) {
  try {
    //const country_name = countryname;
    const apiUrl = 'http://127.0.0.1:5000/';
    const id = Id;
    const mappi = map;
    const locs = locations;
    const namae = namsku;
    const jsonData1 = await fetchJson(apiUrl + 'newCountry/' + count_country);        // PRINTS CORRECT ICAO ON PAGE
    const country_name = jsonData1['country_name'];
    const correctStr = jsonData1['correct'];
    let guessNum = jsonData1['guesses'];
    const count = jsonData1['country_num'];
    const lista = jsonData1['lista'];
    let points = jsonData1['points'];
    let sound = new Audio();
    const button1 = document.getElementById('sound_button');
    button1.addEventListener('click', playSound);

    function playSound() {
      document.getElementById('sound_button').src = '';
      sound.src = `Äänitiedostot/${country_name}.mp3`;
      sound.play();
      console.log(sound);
    }

    //console.log('Maalistan pituus: ' + lista.length);
    const correctCountry = document.createTextNode(`${correctStr}`);
    const correct = document.createTextNode(
        `Question number ${count} / 5`);
    document.getElementById('correct').appendChild(correct);
    document.getElementById('correct');
    const target = document.getElementById('target');

    for (let i = 0; i < locations.length; i++) {
      const marker = L.marker([locations[i][1], locations[i][2]]).addTo(map);
      //--------------------------------------------------------------------------- Pop-upit alkaa
      const popupContent = document.createElement('div');
      const h4 = document.createElement('h4');
      h4.innerHTML = namae[i][0];
      popupContent.append(h4);
      const p = document.createElement('p');
      popupContent.append(p);
      marker.bindPopup(popupContent);
      marker.on('mouseover', function(e) {
        this.openPopup();
      });
      marker.on('mouseout', function(e) {
        this.closePopup();
      });
      //--------------------------------------------------------------------------- Pop-upit loppuu
      marker.addEventListener('click', async function(evt) {
        if (guessNum < 5) {
          //console.log('Klikkaus');
          let guess = locations[i][0];
          //console.log('Arvauksesi: ' + guess);
          const result = await fetchJson(
              apiUrl + 'guess/' + id + '/' + guess + '/' + correctStr + '/' +
              guessNum +
              '/' + points);                                                        // GOES TO ILE'S FUNCTION fetchJson
          guessNum = result['guesses'];                                              // AND CHECKS IF CORRECT
          points = result['point'];
          const distance = result['distance'];                                  // distance between guess and correct
          console.log(distance);
          //console.log('Arvaus nro: ' + result['guesses']);
          let p = document.createTextNode(
              `${result['message']}`);

          if (`${result['check']}` === 'true') {
            console.log('Hyvä, sait ' + points + ' p');
            document.getElementById('correct').innerHTML = '';
            document.getElementById('target').innerHTML = '';
            console.log('Oikein, total points: ' + result['total_points']);
            if (count < 5) {                                                       // IF MAITA JÄLJELLÄ
              button1.removeEventListener('click', playSound);
              start(id, count, locs, mappi, namae, country_name);                  // BACK TO START
            }

          } else {
            //console.log('Väärin, voit saada ' + points + ' p');
            document.getElementById('target').innerHTML = '';
            if (guessNum === 5) {
              document.getElementById('correct').innerHTML = '';
              document.getElementById('target').innerHTML = '';
              p = document.createTextNode(`${result['guesses_used_msg']}`);
              console.log('Väärin, total points: ' + result['total_points']);
              const totalpointsp = result['total_points']


              if (count < 5) {                                                     // IF MAITA JÄLJELLÄ
                button1.removeEventListener('click', playSound);
                start(id, count, locs, mappi, namae, country_name);                // BACK TO START
              }
              if (count == 5) {
                const textfield = document.getElementById("text-p")
                textfield.innerText = "Game over! You got a total of "+ totalpointsp +" points"
                showResults();
              }
            }
          }
          //target.appendChild(p);
          //target.appendChild(s)
            target.appendChild(p);

        }
      });

    }
  } catch (error) {
    console.log(error);
  }

}




  const dialog = document.getElementsByTagName("dialog")
  async function openDialog() {
    const apiUrl = 'http://127.0.0.1:5000/';
    const score = await fetchJson(apiUrl + 'scoreboard/');
    const tulokset = score["totals"]
    const usernames = score["usernames"]
    const ids = score["ids"]
    //console.log(tulokset, usernames, ids)
    const scores = document.getElementById("player-scores")
    scores.innerHTML = "";
    for (let i=0; i<ids.length; i++) {
      const br = document.createElement("br")
      const section = document.createElement("section")
      const numbers = document.createElement("div")
      const player_print = document.createElement("div")
      const score_print = document.createElement("div")

      if (i < 9) {

        numbers.innerText = "0" + (i+1) + ".";

      }
      else
      {
        numbers.innerText = i + 1 + ".";
      }

      numbers.className = "number-s";
      player_print.className = "player_print-s";
      score_print.className = "score_print-s";
      player_print.innerText = usernames[i] ;
      score_print.innerText = tulokset[i]+' p';
      scores.appendChild(section)
      scores.appendChild(br)
      section.appendChild(numbers)
      section.appendChild(player_print)
      section.appendChild(score_print)
    }
    dialog[0].showModal();

}
const span = document.getElementsByTagName("span");

span[0].onclick = function() {
    dialog[0].close();
}

function showResults() {
  dialog[1].showModal();
}
  span[1].onclick = function () {
    dialog[1].close();
  }
