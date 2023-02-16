function addTrack (track) {
  
  let album = track.album
  let cover_url = track.cover_url
  let artists = track.artists
  let title = track.title

  let div = document.createElement('div')
  div.className = 'track-card'
  div.dataset.uri = track.uri
  div.dataset.url = track.track_url
  
  let base = 
    `<img class="track-image" src="${cover_url}" alt="">
      
      
          <div class="track-info">
              <div class="track-title">${title}</div>
              <div class="track-artists">${artists}</div>
          </div>
          <div class="track-album">${album}</div>
      <div class="track-controls">
          <a href="#" class="track-delete">x</a>
          <a href="#" class="track-share">+</a>
          
      </div>`

  div.innerHTML = base

  let send = document.getElementById('send')
  send.insertAdjacentElement('beforebegin', div)
};

let audio, current
 

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
    event.target.parentElement.parentElement.remove()
    
    fetch(`/delete_track/${uri}`)
  
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
    let instrumentalness = document.getElementById('track-instrumentalness').value
    let length = document.getElementById('playlist-length').value
    let prompt = document.getElementById('input-sentence').value
    
    let formData = new FormData();
    formData.append('input-sentence', prompt);
    formData.append("test", "test value")
    
    fetch(`/update_options`,
     {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body : JSON.stringify( {
          'popularity': popularity,
          'instrumentalness' : instrumentalness,
          'length': length,
          'prompt': prompt
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
    
    fetch(`/send_playlist/${playlistName}/${public}/${description}`)
      .then(response => console.log(response))

  }
  if (event.target.matches('.track-link')) {
    let trackUrl = event.target.parentElement.parentElement.dataset.url
    window.open(trackUrl, '_blank');
  }

  if (audio != undefined && !audio.paused && event.target != current) {
    audio.pause()
  }

  if (event.target.matches('.track-image')) {
    
    if (event.target != current){
      
      current = event.target 
      let audioUrl = event.target.parentElement.dataset.preview
      if (audioUrl == "None") {
        return
      }
      audio = new Audio(audioUrl)
      audio.play()

    } else if (!audio.paused) {
      audio.pause()
    } else if (audio.paused) {
      audio.play()
    }
  }
      
});



