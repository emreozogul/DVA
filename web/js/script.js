var initialSettings = {
    init: function () {
        initialSettings.setTitle();
        initialSettings.sayHello();
    },
    setTitle: function () {
        eel.set_title()().then(function (value) {
            $("h1").text(value);
        });
    },
    sayHello: function () {
        $("#submit-button").on('click', function () {
            eel.say_hello_py($("#exampleInputEmail1").val())
            initialSettings.loadUsers();
            return false
        });
    },
    loadUsers: function () {
        eel.get_users()().then(function (users) {
            console.log(users);
            var trHTML = '';
            $.each(users, function (i, user) {
                trHTML += '<tr><td>' + user.email + '</td><td>' + user.password + '</td><td>';
            });
            $('#table-body').empty().append(trHTML);
        })
    },
};


$(document).ready(function () {
    initialSettings.init();
}
);
