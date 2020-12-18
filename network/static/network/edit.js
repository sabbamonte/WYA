  
// load the DOM first
document.addEventListener('DOMContentLoaded', function() {

    // put buttons for edit, like and delete_post in a variable
    listen = document.querySelectorAll('.edit');
    likes = document.querySelectorAll('.like');
    delete_posts = document.querySelectorAll('.delete-post')

    // start edit function when button clicked
    listen.forEach((form) => {
        form.addEventListener('click', () => {
            console.log(form.name)
            edit(form.name)
        });
    })  
    
    // start plus_count and likey function when clicked and it's a "like"
    likes.forEach((like) => {
        like.addEventListener('click', () => {
            console.log(like)
            console.log(like.id)
            like_id = like.id
            if (like.id === 'like') {
                console.log(like.id)
                plus_count(like.name)
                likey(like.name)
                
                
            }
            // do the opposite of the plus count if it's an "unlike"
            else {
                console.log(like.id)
                minus_count(like.name)
                likey(like.name)
              
            }
            
        });
    });

    // start delete_post function when button clicked
    delete_posts.forEach((post) => {
        post.addEventListener('click', () => {
            delete_post(post.id)
        })
        
    })
});

    function edit(post_id) {

        // fetch the right post
        fetch(`/edit/${post_id}`)
        .then(response => response.json())
        .then(posts => {

            // create textarea and prepopulate with existing post to edit it and hide the edit button
            Array.prototype.forEach.call(posts.post, post => {
                document.querySelector(`#disable_post-${post.id}`).innerHTML = `<form id="save"> <textarea rows="5" cols="50" id="newpost">${post.post}</textarea> <br> <button class="btn btn-dark" type="submit"> Save </button></form>`;
                document.querySelector(`.button-view-${post.id}`).style.display = 'none';

                // save edited post when submitted
                document.querySelector('#save').onsubmit = function() {
                    fetch(`/edit/${post_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            post: document.querySelector('#newpost').value
                        })
                    });
                }
            });    
        
        });
    }

    function likey(post_id){

        // find the current username
        const username = JSON.parse(document.getElementById('username').textContent);
        
        // fetch the right post and add username to likes
        fetch(`/likes/${post_id}`, {
            
            method: 'PUT',
            body: JSON.stringify({
                likes: username
            })
        });
    }

    function plus_count(post_id) {

        // find the current counter and add 1 to it
        var counter = document.querySelector(`.count-${post_id}`).innerHTML;
        new_counter = Number(counter) + Number(1)
        
        // fetch the count and set it to new one
        fetch(`/count/${post_id}`, {
            method: "PUT",
            body: JSON.stringify ({
                counter: new_counter
            })
        })

        // set the innerHTML of current counter to new counter
        document.querySelector(`.count-${post_id}`).innerHTML = new_counter;

        // toggle unlike button
        document.querySelector(`.like-view-${post_id}`).innerHTML = `<button class="like button btn btn-dark" name="{{post.id}}" id="unlike-${post_id}"> Unlike </button>`
        document.querySelector(`#unlike-${post_id}`).addEventListener('click', () => {
            minus_count(post_id)
            likey(post_id)
        })
    }

    function minus_count(post_id) {
        
        // find the current counter and subtract 1 from it
        var counter = document.querySelector(`.count-${post_id}`).innerHTML;
        new_counter = Number(counter) - Number(1)

         // fetch the count and set it to new one
        fetch(`/count/${post_id}`, {
            method: "PUT",
            body: JSON.stringify ({
                counter: new_counter
            })
        })

        // set the innerHTML of current counter to new counter
        document.querySelector(`.count-${post_id}`).innerHTML = new_counter;

        // toggle like button
        document.querySelector(`.like-view-${post_id}`).innerHTML = `<button class="like button btn btn-dark" name="{{post.id}}" id="like-${post_id}"> Like </button>`
        document.querySelector(`#like-${post_id}`).addEventListener('click', () => {
            plus_count(post_id)
            likey(post_id)
        }) 
    }

    // fetch the right post and send the post's id to views.py to delete
    function delete_post(post_id) {
        fetch(`/delete/${post_id}`, {
            method: "DELETE",
            body: JSON.stringify ({
                id: post_id
            })  
        })

        // remove the post
        document.getElementById(`${post_id}`).remove();
    }

    
    