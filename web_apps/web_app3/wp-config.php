<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'web_app_3' );

/** MySQL database username */
define( 'DB_USER', 'root' );

/** MySQL database password */
define( 'DB_PASSWORD', 'tmyn1881' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         '1-$*8X+L?l=<]4gA_(v@c)q#IGB{uFHluI]L!y`=L<U1T)Me;}34|;E6E0#U~tM6' );
define( 'SECURE_AUTH_KEY',  ' IG<n,-J.|}u|Uig;]v(1_tWubJ!+&v4_pWTItf{b,21^^ZqNs]}i4MA*G*iK.<:' );
define( 'LOGGED_IN_KEY',    'z5T?qe_;_c|ZBjvcHxyou9N970B{7177:f&nE4)-QfXwXCd=HcZ6x$ORZ<ZeUqi3' );
define( 'NONCE_KEY',        'iq 1Ar4)tj/y5|9F75b9Y}fOHreQokZS5JD:xU@j~Wh9agJnw{u]`<-D0bWqPL%:' );
define( 'AUTH_SALT',        ']Emh6@u59#5zLf}Ci!RL+.0paLPny~m|TzpI|%]XHWnB#9j&9kuQVmwUT0$+AU@9' );
define( 'SECURE_AUTH_SALT', '0Z<a}<zJg@m}vJib<N_`XQd~)Se0bZZ,a,ln<z=utU#D:^5}v>#=9$#Ppk>3r$7J' );
define( 'LOGGED_IN_SALT',   'yt_ry}IkD2;[N> 0@X;,BW)h>#Ds!f XH[)gH~K:Yi?-64F]rym;KVy],|yn*q;)' );
define( 'NONCE_SALT',       ')wA)CFyw%Y3J5yT;FwVAfbra6.!%RB,q4mTU??S$v)?we7bV|s~8Elywh43Mu(uc' );

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define( 'WP_DEBUG', false );

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', dirname( __FILE__ ) . '/' );
}

/** Sets up WordPress vars and included files. */
require_once( ABSPATH . 'wp-settings.php' );
