exports.config =
  paths:
    public: '../backend/static/'
  files:
    javascripts:
      joinTo:
        '../../backend/static/javascripts/app.js': /^app/
        '../../backend/static/javascripts/vendor.js': /^(?!app)/
      order:
        before: [
          'bower_components/jquery/dist/jquery.js'
        ]

    stylesheets:
      joinTo: '../../backend/static/stylesheets/style.css'

  sourceMaps: false