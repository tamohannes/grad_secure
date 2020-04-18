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
define('DB_NAME', 'web_app_8');

/** MySQL database username */
define('DB_USER', 'root');

/** MySQL database password */
define('DB_PASSWORD', 'tmyn1881');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8mb4');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'LKzBM5QG$o^Sp&ouL%mt-9#(l(]I)@1qe{}, F,yvLI}A@R)`Pd[yHL$VLkj>J%j');
define('SECURE_AUTH_KEY',  '5gu7vwXc*lk_5i/mBmMkS5 !izI1f#6,wTmc{KyESo^jM2QDx`3%9sJ?&nR^T`kj');
define('LOGGED_IN_KEY',    '7VU0eq1AvXJIi9DU(knaEMM5UXP`LU]QZ{pOMEx%e<[JO`Mv,6$g3YKLKbq4y5Je');
define('NONCE_KEY',        '>ahr-|gy7a<w?V=}@fFH!hl+v?hp M:o5Vm)+hgZ)s2v,>FLTDLcMS=MoXA0mqj3');
define('AUTH_SALT',        '@w;ZyRw$xOMCjlqtCx5buM1|Y{6$w.=e9^{hG~LrS}<EIbS3UEj|if].]Is;KABa');
define('SECURE_AUTH_SALT', '^RJD`I9Xpp2G)/^R7&:xb[;U9*RSm1rWIr~aj[B392$wW5f~FckfZ7A, 8st.>Il');
define('LOGGED_IN_SALT',   'ae]3DkX>c*5@cAhm4&hPCsV8W/,!;O6q7|F#J_Yh5;2TU$|.zHG.@ufwql cp*Iu');
define('NONCE_SALT',       'c-5ji]. |IB;d&CB$Ke[k^T^`#VQdhJ)WMO-.Br%dU63zU~3w65C(#S-z|TGAn>.');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

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
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');

