function setupSocial()
{
	// setup the invite button
	$('#invite-friends').click(function()
		{
			FB.ui({method: 'apprequests', message: 'Do you want to smash your keyboard with me?', title: 'Come play tapotron with me!'});
		}
	);
	
	// setup the friends list (leader board)
	FB.api(
		{
			method: 'fql.query',
			query: 'SELECT uid, first_name, last_name, pic_square FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me()) AND is_app_user = 1'
		},
		function(response)
		{
			displayFriendsDivs(response);
		}
	);
}

function displayFriendsDivs(rows)
{
	for(i = 0; i < rows.length; i++)
	{
		$('#friendslist').append(
		'<div class="friend" id="friend-'+rows[i].uid+'">'
		+rows[i].first_name+'<br/>'
		+'<img src='+rows[i].pic_square+'/>'
		+'</div>');
		
		displayFriendsBestScore(rows[i].uid);
	}
}

function displayFriendsBestScore(uid)
{
	$.get('/getScore/'+uid+'/',
		function(data)
		{
			// Non mais t'est pas bien ?! C'est quoi ce <br/>
			$('#friend-'+uid).append('<br/>'+data);
		}
	);
}

