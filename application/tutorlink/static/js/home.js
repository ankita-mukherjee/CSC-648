document.addEventListener('DOMContentLoaded', function() {
  var subjectCards = document.querySelectorAll('.subject-card');

  subjectCards.forEach(function(subjectCard) {
    subjectCard.addEventListener('click', function() {
      var subjectText = this.textContent.trim();
      window.location.href = '/search/' + encodeURIComponent(subjectText);
    });
  });
});