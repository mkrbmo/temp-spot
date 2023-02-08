



function addTrack (trackObject) {
  let uri = Object.entries(trackObject)[0][0]
  let track = Object.entries(trackObject)[0][1]
   
  let album = track.album
  let cover_url = track.cover_url
  let artists = track.artists
  let title = track.title

  let div = document.createElement('div')
  div.className = 'track-card'
  div.dataset.uri = uri
  
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

document.addEventListener('click', event => {
  if (event.target.matches('#options-button')) {
    document.getElementById('modal-background').style.display = 'block';
  };
  if (event.target.matches('#modal-cancel')) {
    document.getElementById('modal-background').style.display = 'none';
  };
  if (event.target.matches('#modal-submit')) {
    document.getElementById('modal-background').style.display = 'none';
  }

});

document.addEventListener('click', event => {
  if (event.target.matches('.track-delete')) {
      uri = event.target.parentElement.parentElement.dataset.uri
      
      event.target.parentElement.parentElement.remove()
      
      fetch(`/swap_track/${uri}`)
          .then(response => response.json())
          .then(json => addTrack(json))
          
  }
});


