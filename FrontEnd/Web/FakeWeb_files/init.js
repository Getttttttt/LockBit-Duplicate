window.useDefault = false;

function getState(redirectUrl){
    var uri = redirectUrl + '&javax.faces.partial.ajax=true';
    var state;
    parent.$.ajax({
        type: 'get',
        url: uri,
        success: function (res) {
            var parser = new DOMParser();
            var xmlDoc = parser.parseFromString(res, 'text/xml');
            var url = xmlDoc.getElementsByTagName('redirect')[0].getAttribute('url');
            state = parent.getParameterByName('state',url);
        },
        async: false
    });
    return state;
}

window.onload = function () {
    if (window.useDefault || ie8() || getParameterByName('dev')) {
        document.getElementById('default').style.display = 'block';
        var loginIframe = document.getElementById('loginIframe');
        loginIframe.parentNode.removeChild(loginIframe);
        return;
    }


    if (/MicroMessenger/i.test(navigator.userAgent) && /sso\.buaa\.edu\.cn/i.test(window.location.host) && !getParameterByName('noAutoRedirect') && !config.error) {
        var service =  config.service && config.service.href;
        if (service) {
            localStorage.setItem('service', service);
        }
        var state = getState(config.pac4j.filter(function(e){return e.name === 'mc-wx'})[0].href);
        var url = "https://app.buaa.edu.cn/uc/api/oauth/index?response_type=code&appid=200190528091014504&redirect=https%3A%2F%2Fsso.buaa.edu.cn%2Fcas%2Fredirect.html%3Fclient_name%3Dmc-wx&state="+state;
        window.open(url.replace('/clientredirect?', '/cas/redirect.html?'), '_self');
        return;

        //var url = config.pac4j.filter(function(e){return e.name === 'mc-wx'})[0].href;
        //window.open(url, '_self');
        //return;
    }

    if (getParameterByName('hzsso')) {
        var url = config.pac4j.filter(function(e){return e.name === 'cas'})[0].href;
        window.open(url, '_self');
        return;
    }

    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        if (getParameterByName('test')) document.getElementById('loginIframe').src = '/cas/login-mobile-test.html';
        else document.getElementById('loginIframe').src = '/cas/login-mobile.html';
        document.getElementById('default').style.display = 'block';
    } else {
        if (getParameterByName('test')) document.getElementById('loginIframe').src = '/cas/login-normal-test.html';
        else document.getElementById('loginIframe').src = '/cas/login-normal.html';
        document.getElementById('default').style.display = 'none';
    }
};
