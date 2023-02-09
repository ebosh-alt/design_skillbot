
      const checkout = new window.YooMoneyCheckoutWidget({
          confirmation_token: 'ct-2b759ab6-000f-5000-9000-1a6fd83ce42b',
          return_url: 'https://t.me/design_ai_skillbot',
          error_callback: function(error) {
              console.log(error)
          }
      });

      checkout.render('payment-form');
