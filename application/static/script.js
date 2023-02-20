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
          <a href="#" class="track-mixin" data-id="${track.id}">+</a>
          
      </div>`

  div.innerHTML = base

  let send = document.getElementById('send')
  send.insertAdjacentElement('beforebegin', div)
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
}
document.addEventListener('click', event => {
  let audio = document.getElementById('audio-preview')
  
    audio.pause()
  
})


document.addEventListener('click', event => {
  if (event.target.matches('#options-button')) {
    document.getElementById('modal-background').style.display = 'block';
    document.getElementById('options-modal').style.display = 'block';
  };
  if (event.target.matches('.modal-cancel')) {
    document.getElementById('modal-background').style.display = 'none';
    document.getElementById('options-modal').style.display = 'none';
    document.getElementById('playlist-modal').style.display = 'none';
  };
  if (event.target.matches('.modal-submit')) {
    document.getElementById('modal-background').style.display = 'none';
  }
  if (event.target.matches('#send_card')) {
    document.getElementById('modal-background').style.display = 'block';
    document.getElementById('playlist-modal').style.display = 'block';
  }

  if (event.target.matches('.track-delete')) {
    uri = event.target.parentElement.parentElement.dataset.uri
    fetch(`/delete_track/${uri}`)
    .then(response => {
      if (response.statusText == "OK") {
        event.target.parentElement.parentElement.remove()
      }
    })
  
  }
  if (event.target.matches('#track-add')) {
    fetch('/add_track')
    .then(response => response.json())
    .then(track => {
      addTrack(track)
    })
  }

  if (event.target.matches('#options-send')) {
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

          
        
      
  
  }

  if (event.target.matches('#playlist-send')){
    let playlistName = document.getElementById('playlist-name').value
    let description = document.getElementById('playlist-description').value
    let public = document.querySelector('input[name="public"]:checked').value;
    
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
    
      
    }

  if (event.target.matches('.track-title')) {
    let trackUrl = event.target.dataset.url
    window.open(trackUrl, '_blank');
  }
/*
  if (audio.dataset.current != '' && !audio.paused && event.target != current) {
    audio.pause()
  }
*/
  
  if (event.target.matches('.track-image')) {
    let audio = document.getElementById('audio-preview')
    
    if (event.target.dataset.preview != audio.src){
      audio.src = event.target.dataset.preview
      if (audio.src == "None") {
        return
      }
      audio.play()

    } else if (!audio.paused) {
      audio.pause()
    } else if (audio.paused) {
      audio.play()
    }
  }
});

document.addEventListener('click', event => {
  if (event.target.matches('.track-mixin')){
    
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
})


document.addEventListener('keyup', event => {
  if (!event.target.matches('#search-artist')) {
    return
  }
  const ignore = ['ArrowDown', 'ArrowUp', 'ArrowLeft', 'ArrowRight', 'Enter']
  if (!ignore.includes(event.code)) {
    suggest(event.target.value)
  }
})
