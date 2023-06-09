document.addEventListener('DOMContentLoaded', () => {
    //load movies
    const movies_list = document.querySelector('#movies-list')

    fetch('/get_movies')
    .then(response => response.json())
    .then(data => {
        data.movies.forEach(function (each) {
            let movie_box = Object.assign(document.createElement('div'), {
                id: 'movie-box'
            });
    
            movie_box.innerHTML = `
                <div class = 'thumbnail-container'>
                    <a href = '/movie_page?movie_id=${each.id}'>
                        <img src = '${each.thumbnail}' class = 'movie-thumbnail'></img>
                    </a>
                </div>
                <h6>${each.title}</h6>`
    
            movies_list.append(movie_box);
        });
    })
})