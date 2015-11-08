require 'spec_helper'
describe 'static_website_updater' do

  context 'with defaults for all parameters' do
    it { should contain_class('static_website_updater') }
  end
end
