/***** LOGIN/CREATE *****/

$('#switch-to-create').click(function(e){
	e.preventDefault();

	$('#user-login-form').fadeOut(function(){
		$('#user-create-form').fadeIn();
	});
	
});

$('#switch-to-login').click(function(e){
	e.preventDefault();

	$('#user-create-form').fadeOut(function(){
		$('#user-login-form').fadeIn();
	});
});

/****** POST ADMIN ******/

$('.edit-post-link').click(function(e){
	e.preventDefault();

	var id = $(this).attr('data-post-id');

	$.get('/blog/posts/' + id + '/json/', function(result){
		console.log(result);

		$('#submit-button').html('Modify Post');
		$('#cancel-button').show();

		var text = result[0].fields.text
		var title = result[0].fields.title
		var id = result[0].pk
		var author = result[0].fields.author
		var featured_image = result[0].fields.featured_image

		$('#post-form input[name="author"]').val(author);
		$('#post-form input[name="title"]').val(title);
		$('#post-form textarea[name="text"]').val(text);
		$('#post-form input[name="id"]').val(id);

		if (featured_image.length > 0) {
			$('#featured-image-form').attr('src', '/media/' + featured_image).show();
		} else {
			$('#featured-image-form').attr('src', '').hide();
		}
	});
});

$('#cancel-button').click(function(e){
	e.preventDefault();

	$('#post-form input[name="author"]').val(global_author);
	$('#post-form input[name="title"]').val('');
	$('#post-form textarea[name="text"]').val('');
	$('#post-form input[name="id"]').val('');
	$('#featured-image-form').attr('src', '').hide();

	$('#submit-button').html('Create Post');
	$('#cancel-button').hide();

});



/****** DELETE POSTS ******/

$('#posts').on('click', '.delete', function(){

	if (confirm("Are you sure you want to delete this?")){
		var id = $(this).parents('article').attr('id');

		$.ajax({
			url: '/blog/posts/' + id + '/',
			method: 'DELETE',
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"))
			},
			success: function() {
				$('#'+id).remove();
			}
		})
	}

});


/***** LOADING POSTS ******/
var page = 0;

loadPosts(page);

$('#older-posts').click(function(e){
	e.preventDefault();

	page++;
	loadPosts(page);
});

function loadPosts(page) {
	// $('#loader').show();

	$.ajax({
		url: '/blog/post-previews/',
		data: {
			page: page
		},
		success: function(result) {

			if (result.length === 0) {
				$('#post-previews').append("Sorry, No posts found")
				$('#older-posts').hide();
			} else {
				$('#post-previews').append(result);
			}
		}
	})
}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}