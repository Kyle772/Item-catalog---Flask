$(function (){
    userFlow = {
        signOut: function () {
            gapi.load('auth2', function() {
                gapi.auth2.init()
            });
            setTimeout(function () {
                var auth2 = gapi.auth2.getAuthInstance();
                auth2.signOut().then(function () {
                  console.log('User signed out.');
                  window.location.replace("/logout")
                });
            }, 500)
        },
        onSignIn: function (googleUser) {
            console.log("called");
            var access_token = googleUser.getAuthResponse().access_token;

            setTimeout(function () {
                $.ajax({
                  method: "POST",
                  url: "/login-google",
                  data: {
                    'token': access_token
                  },
                  success: function () {
                    console.log("Sign in with google: success");
                    window.location.replace("/");
                  }
                })
                .fail(function () {
                  console.log("Sign in with google: fail");
                })
                .done(function () {
                  console.log("Sign in with google: done");
                });

                console.log("Done");
            }, 1000)
        }

    }

    $("a[data-button='signOut']").on('click', function() {
        userFlow.signOut();
    });
});
