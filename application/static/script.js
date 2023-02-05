let tracks = []


function importVariables (queue) {
  tracks = queue;
}



document.addEventListener('click', event => {
  if (!event.target.matches('.track-delete')) {
    return
  }
  event.target.parentElement.parentElement.remove()

  if (tracks.length < 1) {
    return
  }
  let track = tracks.pop()

  let album = track.album
  let cover_url = track.cover_url
  let artists = track.artists
  let title = track.title

  let div = document.createElement('div')
  div.className = 'track-card'
  
  let base = `
    
            
            
            <img class="track-image" src="${cover_url}" alt="">
            
            
                <div class="track-info">
                    <div class="track-title">${title}</div>
                    <div class="track-artists">${artists}</div>
                </div>
                <div class="track-album">${album}</div>
            <div class="track-controls">
                <a href="#" class="track-delete">x</a>
                <a href="#" class="track-share">+</a>
                
            </div>
        
    `
  div.innerHTML = base

  let send = document.getElementById('send')
  send.insertAdjacentElement('beforebegin', div)

});



