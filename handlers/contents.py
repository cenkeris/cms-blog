from flask import request, render_template, url_for, flash, session
from werkzeug.utils import redirect

from services.contents import get_contents_from_api, get_contents_from_url, get_contents_from_about, \
    get_contents_from_contact, get_contents_from_login, get_token, get_user, update_content


def init_handler(app):
    @app.route('/')
    def get_contents():

        page = request.args.get('page', 1)

        page = int(page)

        contents = get_contents_from_api(page)
        user = session.get('user')
        if not contents:
            last_item = {}
            return render_template('home.html', posts=contents, last_item=last_item, user=user)

        last_item = contents[0]
        return render_template('home.html', posts=contents, last_item=last_item, user=user)

    @app.route('/url/<url>', methods=['GET', 'POST'])
    def content_detail(url):
        if not url:
            return redirect(url_for('index'))

        user = session.get('user')
        post = get_contents_from_url(url)
        if request.method == 'POST':
            comment = request.form.get('comment')
            comment = comment.strip()
            if not comment:
                return render_template('content.html', post=post, user=user)

            post = update_content(post, comment)
            return render_template('content.html', post=post, user=user, comment=comment)

        return render_template('content.html', post=post, user=user)

    @app.route('/about')
    def content_about():

        user = session.get('user')
        post = get_contents_from_about('hakkimda')
        return render_template('hakkimda.html', post=post, user=user)

    @app.route('/contact')
    def content_contact():

        user = session.get('user')
        post = get_contents_from_contact('iletisim')
        return render_template('iletisim.html', post=post, user=user)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            credentials = {
                'username': username,
                'password': password
            }
            token = get_token(credentials)
            if not token:
                flash("Kullanıcı adı ya da parola hatalı.")
                return redirect(url_for('login'))

            user = get_user(token)

            if not user:
                flash("Kullanıcı logout edildi.")
                return redirect(url_for('login'))

            session['user'] = user
            session['token'] = token
            session['credentials'] = credentials

            return redirect(url_for('get_contents'))

            #: alınan body'i tokens apisine gönder
            #: 201 dönerse /me apisine git kullanıcıyı çek
            #: kullanıcıyı ve token'ı session'a kaydet
            #: eger session'da bir kullanıcı ve token varsa kullanıcıyı index'e gönder
            #: her requestte session'da user var mı kontrolü eklenecek.
        post = get_contents_from_login('giris')
        return render_template('giris.html', post=post)

    @app.route('/logout')
    def logout():
        session.pop('user')
        session.pop('token')

        return redirect('login')

