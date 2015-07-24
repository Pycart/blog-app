loadPosts();

$('#load-posts').click(loadPosts);

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

$('#post-form').submit(function(e){
	e.preventDefault();

	var title = $('#post-form input[name="title"]').val();
	var text = $('#post-form textarea[name="post-content"').val();
	var csrf = $('#post-form input[name="csrfmiddlewaretoken"]').val();

	$.ajax({
		url: '/blog/create-post/',
		method: 'POST',
		data: {
			title: title,
			text: text,
			csrfmiddlewaretoken: csrf
		},
		success: function(result) {
			$('#post-form input[name="title"]').val('');
			$('#post-form textarea[name="post-content"').val('');

			$('#posts').prepend(result);
		}
	})

});



function loadPosts() {
	$('#loader').show();

	$.ajax({
		url: '/blog/posts',
		success: function(result) {
			$('#loader').hide();

			$(result).each(function(){
				console.log(this);

				var article = "<article id='" + this.pk + "'><h1>" +
				this.fields.title + "</h1>" +
				this.fields.text + 
				"<footer><p>Posted On: " +
				this.fields.date_posted + "</p><button class='delete'>Delete</button></footer></article>";

				$('#posts').append(article);
			});
		}
	})
}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}