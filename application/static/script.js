function addTrack (track) {
  let div = document.createElement('div')
  div.className = 'track-card'
  div.dataset.uri = track.uri
  div.dataset.url = track.track_url
  
  let base = 
    `<img class="track-image" src="${track.cover_url}" alt="album cover" data-preview="${track.preview_url}">
      
      
          <div class="track-info">
              <div class="track-title" data-url="${track.track_url}">${track.title}</div>
              <div class="track-artists">${track.artists}</div>
          </div>
          <div class="track-album">${track.album}</div>
      <div class="track-controls">
          <a href="#" class="track-delete">x</a>
          <a href="#" class="track-options" data-id="${track.id}">+</a>
          
      </div>`

  div.innerHTML = base

  let legend = document.getElementById('legend')
  legend.insertAdjacentElement('afterend', div)
};


function suggest(artist) {
  if (artist == '' || artist.trim() == '') {
    return
  }
  fetch(`/suggest/?q=${artist}`)
  .then(function (response) {
      return response.json()
  })
  .then(suggestions => {
    
    let suggestion_cards = document.getElementsByClassName('suggestion')
    for (let i = 0; i<3; i++) {
      suggestion_cards[i].value = suggestions[i][0]
      suggestion_cards[i].innerHTML = suggestions[i][0]
    }
  })
};

/*
**  ------------
**  AUDIO HANDLING
**  -------------
*/

function initializeAudio(target) {
  let url = target.dataset.preview
  target.parentElement.classList.add('playing')
  target.parentElement.classList.add('record')
  if (url == 'None') {
    return
  }
  let audio = document.createElement('audio')
  audio.id = 'audio-preview'
  audio.src = url
  target.insertAdjacentElement('afterend', audio)
  audio.play()
};

function resetAudio() {
  audio.remove()
  let containers = document.querySelectorAll('.track-image-container')
    containers.forEach((container) => {
        container.classList.remove('playing')
        container.classList.remove('record')
    })
}
document.addEventListener('click', event => {
  let e = event.target
  let p = event.target.parentElement
  let audio = document.getElementById('audio-preview')
  if (audio && !e.matches('.track-image')) {
    resetAudio()
  }
  else if (e.matches('.track-image')) {
    resetAudio()
    if (e.dataset.preview == 'None') {
      e.nextElementSibling.style.display = 'block'
      setTimeout(() => {
        e.nextElementSibling.style.display = 'none'
      }, "3000")
      return
    } else if (!audio) {
      initializeAudio(e)
    } else if (audio && audio.src == e.dataset.preview) {
      
      if (audio.paused) {
        audio.play();
        p.classList.add('playing')
      }
      else if (!audio.paused) {
        audio.pause()
        p.classList.remove('playing')
      }
    } else if (audio && audio.src != e.dataset.preview) {
      resetAudio()
      initializeAudio(e)
    }
  }


  else if (event.target.matches('.track-delete')) {
    uri = event.target.parentElement.parentElement.dataset.uri
    fetch(`/delete_track/${uri}`)
    .then(response => {
      if (response.statusText == "OK") {
        event.target.parentElement.parentElement.remove()
      }
    })
  }
  else if (event.target.matches('#mix-song-button')){
    
    let id = event.target.dataset.id
    let uri = event.target.parentElement.parentElement.dataset.uri
    
    fetch(`/mixin_track/${id}/${uri}`)
    .then(response => response.json())
    .then(newTracks => {
      let cards = document.querySelectorAll('.track-card')
      cards.forEach((card) => {
          card.remove()
      })
      for (let newTrack in newTracks) {
        addTrack(newTracks[newTrack])
      }
    })
  }

});


document.addEventListener('click', event => {
  if (event.target.matches('#form-options-button')) {
    document.getElementById('modal-background').style.display = 'block';
    document.getElementById('options-modal').style.display = 'block';
    let popularity = document.getElementById('track-popularity').value
    document.getElementById('popularity-range').style['background-size'] = popularity + '%'
    document.getElementById('popularity-indicator').innerHTML = popularity
    let length = document.getElementById('playlist-length').value
    document.getElementById('length-range').style['background-size'] = (length*5-50) + '%'
    document.getElementById('length-indicator').innerHTML = length
  }
  else if (event.target.matches('#modal-cancel') || event.target.matches('.modal-button')) {
    document.getElementById('modal-background').style.display = 'none';
    document.getElementById('options-modal').style.display = 'none';
    document.getElementById('playlist-modal').style.display = 'none';
    document.getElementById('track-modal').style.display = 'none';
  }
  else if (event.target.matches('#send-button')) {
    document.getElementById('modal-background').style.display = 'block';
    document.getElementById('playlist-modal').style.display = 'block';
  }
  else if (event.target.matches('.track-options')) {
    document.getElementById('modal-background').style.display = 'block';
    document.getElementById('track-modal').style.display = 'block';
  }

  else if (event.target.matches('#track-add-button')) {
    fetch('/add_track')
    .then(response => response.json())
    .then(track => {
      addTrack(track)
    })
  };

  if (event.target.matches('#options-submit')) {
    let popularity = document.getElementById('track-popularity').value
    let length = document.getElementById('playlist-length').value
    
    fetch(`/update_options`,
     {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body : JSON.stringify( {
          'popularity': popularity,
          'length': length
        })
      }).then(response => response.json())
        .then(newTracks => {
          let cards = document.querySelectorAll('.track-card')
          cards.forEach((card) =>
            card.remove()
          )
          for (let newTrack in newTracks) {
            addTrack(newTracks[newTrack])
          }
        })

          
        
      
  
  };

  if (event.target.matches('#playlist-send')){
    let playlistName = document.getElementById('playlist-name').value
    let description = document.getElementById('playlist-description').value
    let public = document.querySelector('input[name="visibility"]:checked').value;
    
    fetch('/send_playlist',
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body : JSON.stringify( {
          'name': playlistName,
          'description': description,
          'public': public
        })
      }).then(response => {
          console.log(response)
        })
    
      
  };
/*
  if (event.target.matches('.track-title')) {
    let trackUrl = event.target.dataset.url
    window.open(trackUrl, '_blank');
  }
*/
  
});
//MIX IN TRACK TO RECCOMENDATION
document.addEventListener('click', event => {

});

window.onload = function() {
  let searchBox = document.getElementById('artist-input')
  if (searchBox) {
    searchBox.addEventListener('keyup', event => {
      const ignore = ['ArrowDown', 'ArrowUp', 'ArrowLeft', 'ArrowRight', 'Enter']
      if (!ignore.includes(event.code)) {
        suggest(event.target.value)
      }
    });
  }
}


//EVENT LISTENER FOR AUDIO PREVIEW
