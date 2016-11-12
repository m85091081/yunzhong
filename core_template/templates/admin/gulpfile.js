'use strict';

var gulp = require('gulp');

var sass = require('gulp-sass');

var rename = require ('gulp-rename');

gulp.task('styles', function () {

    gulp.src('./sass/application.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./css'));

    gulp.src('./sass/application.scss')
        .pipe(sass({
            outputStyle: 'compressed'
        }).on('error', sass.logError))
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('./css'));
});

gulp.task('watch', function () {
    gulp.watch('./sass/*.scss', ['styles']);
});