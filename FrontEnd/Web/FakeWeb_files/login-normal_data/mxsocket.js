function mxsocket(opts) {
    var defaultOpts = {
        domain: "",
        security: false,
        appid: "",
        qrcode_id: 'qrcode',
        qrcode_width: 256,
        qrcode_height: 256,
        debug: false,
        url: "",
        open: null,
        close: null,
        error: null,
        qrcode: null,
        ticket: null,
        smlogin:false
    };
    if (typeof Object.assign != 'function') {
		Object.assign = function(target) {
			'use strict';
			if (target == null) {
				throw new TypeError('Cannot convert undefined or null to object');
			}
			target = Object(target);
			for (var index = 1; index < arguments.length; index++) {
				var source = arguments[index];
			if (source != null) {
				for (var key in source) {
					if (Object.prototype.hasOwnProperty.call(source, key)) {
						target[key] = source[key];
					}
				}
			}
		}
		return target;
		};
	}
    this.opts = Object.assign({}, defaultOpts, opts);
    this.qrcode = new QRCode(document.getElementById(this.opts.qrcode_id), {
        width: this.opts.qrcode_width,
        height: this.opts.qrcode_height
    });
    this.opts.url = (this.opts.security ? "wss" : "ws") + "://" + this.opts.domain + "/sock/qrcode?appid=" + this.opts.appid,
    console.log(99999,this.opts.url)
    this.init();
}

mxsocket.prototype = {
    constructor: mxsocket,
    sock: null,
    qrcode: null,
    timer: null,
    init: function () {

        this.sock = new WebSocket(this.opts.url);
        var self = this;
        this.sock.onopen = function (evt) {
            self.log("socket conneted");
            if (self.opts.open) {
                self.opts.open.call(self, evt);
            }
        };
        this.sock.onclose = function (evt) {
            self.log("socket disconnected");
            if (self.opts.close) {
                self.opts.close.call(self, evt);
            }
            self.socket = null;
        };
        this.sock.onerror = function (evt) {
            self.log("socket error:");
            self.log(evt);
            if (self.opts.error) {
                self.opts.error(evt, 2);
                self.opts.error.call(self, evt);
            }
            self.socket = null;
        };
        this.sock.onmessage = function (message) {
            self.log("message:" + message.data);
            var data = JSON.parse(message.data);
            var evt = data.event;
            if(evt == 'ticket'){
                return self.ticket.call(self, data.data);
            }
            else if (typeof self.opts[evt] == "undefined") {
                self.log("未定义事件：" + evt);
                return;
            }
            self.opts[evt].call(self, data.data);
        }
    },

    callError: function (msg) {
        if (this.opts.error) {
            this.opts.error(msg, 1);
        } else {
            console.error(msg);
        }
    },
    ticket: function (rs) {
        //请求ticket成功后会触发该事件,无需复写
        if(this.timer != null) {
            clearTimeout(this.timer);
        }
        
        var self = this;
        if(self.opts.smlogin){
            this.qrcode.makeCode((this.opts.security ? "https" : "http") + "://" + this.opts.domain + "/site/smloginV2/index?ticket=" + rs.ticket);
        }else{
            this.qrcode.makeCode((this.opts.security ? "https" : "http") + "://" + this.opts.domain + "/site/smlogin/index?ticket=" + rs.ticket);
        }
        if (self.opts.ticket) {
            self.opts.ticket.call(self, rs);
        }

        if (rs.expire) {
            this.timer = setTimeout(function () {
                self.send('ticket');
            }, (rs.expire-1) * 1000);
        }
    },
    send: function (data, error) {
        if (!this.sock) {
            console.error("socket closed");
            return false;
        }
        if (this.sock.readyState != 1) {
            console.error("connection is establishing or closed");
            return false;
        }
        return this.sock.send(data);
    },

    close: function () {
        if (this.sock) {
            this.sock.close();
        }
    },

    log: function (msg) {
        if (typeof this.opts.log == "function") {
            this.opts.log(msg);
        } else if (this.opts.debug) {
            console.log(msg);
        }
    }
}
