FULL_SERVICES = ['appleMusic', 'spotify', 'deezer', 'yandex', 'google', 'youtubeMusic', 'tidal', 'pandora', 'soundcloud', 'napster', 'fanburst', 'vkontakte']

SERVICE_LINKS = [
        'music.apple.com', 
        'open.spotify.com', 
        'deezer.com', 
        'music.yandex.ru',
        'music.youtube.com',
        'play.google.com', 
        'tidal.com', 
        'pandora.com', 
        'soundcloud.com', 
        'napster.com', 
        'fanburst.com'
]

ALIASES = {
            'appleMusic': 'Apple Music',
            'youtubeMusic': 'YouTube Music',
            'yandex': 'Yandex Music',
            'vkontakte': 'VKontakte'
        }

STAT_TYPES = [
             'week count', 'week service', 'week uniq', 'week news',
             'month count', 'yesterday service',
             'last_month count', 'last_week count', 'yesterday type',   
             'month service', 'all service',
             'last_month service', 'last_week service', 'all type',
             'month type', 'week type', 'month uniq',
             'last_month type', 'last_week type',
             'month news', 'all news'
        ]

INSTRUCTIONS_RU = [
        'Для начала отправьте Боту ссылку на песню из своего любимого музыкального сервиса',
        'Бот поддерживает следующие сервисы:\n\nApple Music\nSpotify\nDeezer\nYouTube Music\nYandex\nVKontakte\nGoogle Music\nTidal\nPandora\nSoundcloud\nNapster\nFanburst',
        'Вы можете изменить этот список с помощью команды /edit_serviсes, а так же посмотреть, какие из них у вас сейчас активны - /show_services.',
        'Если Бот добавлен в группу или канал, он будет подменять сообщение, на которое отвечает, если ему предоставить права администратора (отметки "Все пользователи являются администраторами" недостаточно)',
        'Для настройки Бота в канале можно использовать короткие версии команд /show и /edit так же, как и в приватном чате',
        'Чтобы текст, находящийся перед ссылкой, отображался в сообщении - установите /toggle_annotations: on'
]

INSTRUCTIONS_EN = [
        'To use Bot, you need to send him a "share" link from your favorite streaming service',
        'Supported services:\n\nApple Music\nSpotify\nDeezer\nYouTube Music\nYandex\nVKontakte\nGoogle Music\nTidal\nPandora\nSoundcloud\nNapster\nFanburst',
        'You can also change the list of services to which Bot provides links using the /edit_serviсes command or see what services you currently have - /show_services',
        'Bot can delete a message in the group to which it replies. To do this, he must be granted administrator rights (the “All members of the group are administrators” marks are not enough)',
        'If you want to use Bot in your channels, you can use short commands /show and /edit like in the private chats',
        'To display the text in front of the link in the message - set the /toggle_annotations: on'
]