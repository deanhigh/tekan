var gulp = require('gulp');
var bower = require('gulp-bower');

gulp.task('bower', function() {
    return bower();
});

var plugins = require('gulp-load-plugins')();
var runSequence = require('run-sequence');
var pkg = require('./package.json');
var dirs = pkg['h5bp-configs'].directories;

// ---------------------------------------------------------------------
// | Helper tasks                                                      |
// ---------------------------------------------------------------------

gulp.task('clean', function (done) {
    require('del')([
        dirs.dist
    ]).then(function () {
        done();
    });
});

gulp.task('copy', ['copy:src_to_dist']);

gulp.task('copy:bower_components', function () {
    return gulp.src(['bower_components/**/*'])
               .pipe(gulp.dest(dirs.src + '/bower_components/'));
});

gulp.task('copy:src_to_dist', function () {
    return gulp.src([
        // Copy all files excluding main.js
        dirs.src + '/**/*'
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
        'bower',
        'copy:bower_components',
        'copy',
    done);
});

gulp.task('default', ['build']);
