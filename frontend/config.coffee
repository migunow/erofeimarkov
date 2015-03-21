exports.config =
  paths:
    public: '../app/static/'
  files:
    javascripts:
      joinTo:
        '../../app/static/javascripts/app.js': /^app/
        '../../app/static/javascripts/vendor.js': /^(?!app)/
      order:
        before: [
          'bower_components/jquery/dist/jquery.js'
        ]

    stylesheets:
      joinTo: '../../app/static/stylesheets/style.css'

  sourceMaps: false
