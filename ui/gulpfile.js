var fs = require('fs');
var path = require('path');
var gulp = require('gulp');

// Load all gulp plugins automatically
// and attach them to the `plugins` object
var plugins = require('gulp-load-plugins')();

// Temporary solution until gulp 4
// https://github.com/gulpjs/gulp/issues/355
var runSequence = require('run-sequence');

var pkg = require('./package.json');
var dirs = pkg['h5bp-configs'].directories;

// ---------------------------------------------------------------------
// | Helper tasks                                                      |
// ---------------------------------------------------------------------

gulp.task('clean', function (done) {
    require('del')([
        dirs.archive,
        dirs.dist
    ]).then(function () {
        done();
    });
});

gulp.task('copy', [
    'copy:jquery',
    'copy:bootstrap',
    'copy:src_to_dist'
]);

gulp.task('copy:jquery', function () {
    return gulp.src(['node_modules/jquery/dist/*'])
               .pipe(gulp.dest(dirs.src + '/js/vendor/'));
});

gulp.task('copy:bootstrap', ['copy:bootstrap_css', 'copy:bootstrap_js']);

gulp.task('copy:bootstrap_css', function () {
    return gulp.src('node_modules/bootstrap/dist/css/*')
               .pipe(gulp.dest(dirs.src+'/css/vendor/'));
});

gulp.task('copy:bootstrap_js', function () {
    return gulp.src('node_modules/bootstrap/dist/js/*')
        .pipe(gulp.dest(dirs.src+'/js/vendor/'));
});

gulp.task('copy:src_to_dist', function () {
    return gulp.src([
        // Copy all files
        dirs.src + '/**/*',
    ],
        {
            // Include hidden files by default
            dot: true
        }).pipe(gulp.dest(dirs.dist));
});

// ---------------------------------------------------------------------
// | Main tasks                                                        |
// ---------------------------------------------------------------------
gulp.task('build', function (done) {
    runSequence(
        ['clean'],
        'copy',
    done);
});

gulp.task('default', ['build']);
