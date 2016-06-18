'use strict';
var gulp = require('gulp');
var del = require('del');
var path = require('path');
var gutil = require('gulp-util');
// Load plugins
var $ = require('gulp-load-plugins')();
var browserify = require('browserify');
var watchify = require('watchify');
var source = require('vinyl-source-stream'),
  sourceFile = './app/scripts/index.js',
  destFolder = './dist/scripts',
  destFileName = 'index.js';
var browserSync = require('browser-sync');
var reload = browserSync.reload;

var plumber = require('gulp-plumber');
var postcss = require('gulp-postcss'),
  sourcemaps = require('gulp-sourcemaps'),
  lost = require('lost');
var sass = require('gulp-sass');
var prefix = require('gulp-autoprefixer');
var fontAwesome = require('node-font-awesome');

// Styles
gulp.task('styles', ['sass', 'css']);

gulp.task('css', function() {
  return gulp.src('app/styles/font-awesome.min.css')
    .pipe(gulp.dest('dist/css'))
    .pipe(gulp.dest('../css/'))
    .pipe(browserSync.reload({
      stream: true
    }))
});

gulp.task('sass', function() {
  return gulp.src('app/styles/main.scss')
    .pipe(plumber(function(error) {
      gutil.log(error.message);
      this.emit('end');
    }))
    .pipe(sass({
      includePaths: ['scss', fontAwesome.scssPath],
      onError: browserSync.notify
    }))
    .pipe(sourcemaps.init())
    .pipe(postcss([
      lost()
    ]))
    .pipe(sourcemaps.write('./'))
    .pipe(prefix(['last 15 versions', '> 1%', 'ie 8', 'ie 7'], {
      cascade: true
    }))
    .pipe(gulp.dest('dist/css'))
    .pipe(gulp.dest('../css/'))
    .pipe(browserSync.reload({
      stream: true
    }))
});

var bundler = watchify(browserify({
  entries: [sourceFile],
  debug: true,
  insertGlobals: true,
  cache: {},
  packageCache: {},
  fullPaths: true
}));

bundler.on('update', rebundle);
bundler.on('log', $.util.log);

function rebundle() {
  return bundler.bundle()
    // log errors if they happen
    .on('error', $.util.log.bind($.util, 'Browserify Error'))
    .pipe(source(destFileName))
    .pipe(gulp.dest(destFolder))
    //.pipe(gulp.dest("../js/"))
    .on('end', function() {
      reload();
    });
}

// Scripts
gulp.task('scripts', rebundle);

gulp.task('buildScripts', function() {
  return browserify(sourceFile)
    .bundle()
    .pipe(source(destFileName))
    .pipe(gulp.dest('dist/scripts'))
    .pipe(gulp.dest('../js/'));
});




// HTML
gulp.task('html', function() {
  return gulp.src('app/*.html')
    .pipe($.useref())
    //.pipe(gulp.dest('dist'))
    .pipe($.size());
});

// Images
gulp.task('images', function() {
  return gulp.src('app/images/**/*')
    .pipe($.cache($.imagemin({
      optimizationLevel: 3,
      progressive: true,
      interlaced: true
    })))
    .pipe(gulp.dest('dist/images'))
    .pipe(gulp.dest('../img'))
    .pipe($.size());
});

// Fonts
gulp.task('fonts', function() {
  gulp.src(fontAwesome.fonts)
    .pipe(gulp.dest('./app/fonts'));
  return gulp.src(require('main-bower-files')({
      filter: '**/*.{eot,svg,ttf,woff,woff2}'
    }).concat('app/fonts/**/*'))
    .pipe(gulp.dest('dist/fonts'))
    .pipe(gulp.dest('../fonts'))

});

// Clean
gulp.task('clean', function(cb) {
  $.cache.clearAll();
  cb(del.sync(['dist/styles', 'dist/scripts', 'dist/images']));
});

// Bundle
gulp.task('bundle', ['styles', 'scripts', 'bower'], function() {
  return gulp.src('./app/*.html')
    .pipe($.useref.assets())
    .pipe($.useref.restore())
    .pipe($.useref())
    // .pipe(gulp.dest('dist'));
});

gulp.task('buildBundle', ['styles', 'buildScripts', 'moveLibraries', 'bower'], function() {
  return gulp.src('./app/*.html')
    .pipe($.useref.assets())
    .pipe($.useref.restore())
    .pipe($.useref())
    // .pipe(gulp.dest('dist'));
});

// Move JS Files and Libraries
gulp.task('moveLibraries', ['clean'], function() {
  // the base option sets the relative root for the set of files,
  // preserving the folder structure
  gulp.src(['./app/scripts/**/*.js'], {
    base: './app/scripts/'
  })
    .pipe(gulp.dest('dist/scripts'));
});


// Bower helper
gulp.task('bower', function() {
  gulp.src('app/bower_components/**/*.js', {
    base: 'app/bower_components'
  })
    .pipe(gulp.dest('dist/bower_components/'));

});

gulp.task('json', function() {
  gulp.src('app/scripts/json/**/*.json', {
    base: 'app/scripts'
  })
    .pipe(gulp.dest('dist/scripts/'));
});

// Robots.txt and favicon.ico
gulp.task('extras', function() {
  return gulp.src(['app/*.txt', 'app/*.ico'])
    .pipe(gulp.dest('dist/'))
    .pipe($.size());
});

// Watch
gulp.task('watch', ['html', 'fonts', 'bundle'], function() {

  browserSync({
    notify: true,
    logPrefix: 'BS',
    // Run as an https by uncommenting 'https: true'
    // Note: this uses an unsigned certificate which on first access
    //       will present a certificate warning in the browser.
    // https: true,
    server: ['dist', 'app']
  });

  // Watch .json files
  gulp.watch('app/scripts/**/*.json', ['json']);

  gulp.watch(['app/styles/**/*.scss', 'app/styles/**/*.css'], ['styles', 'scripts', reload]);


  // Watch image files
  gulp.watch('app/images/**/*', reload);
});

// Build
gulp.task('build', ['html', 'buildBundle', 'images', 'fonts', 'extras'], function() {
  gulp.src('dist/scripts/index.js')
    .pipe($.uglify())
    .pipe($.stripDebug())
    .pipe(gulp.dest('dist/scripts'))
    .pipe(gulp.dest('../js'));
});

// Debug build
gulp.task('debugBuild', ['html', 'buildBundle', 'images', 'fonts', 'extras'], function() {
  gulp.src('dist/scripts/index.js')
    .pipe(gulp.dest('dist/scripts'))
    .pipe(gulp.dest('../js'));
});

// Default task
gulp.task('default', ['clean', 'build']);