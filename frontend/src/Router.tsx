import { Route, Routes, BrowserRouter } from 'react-router-dom';

import { AuthProvider, RequireAuth } from './components/Authentication';

import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';
import { AboutPage } from './pages/AboutPage';
import { InterfacePage } from './pages/InterfacePage';
import { ReportPage } from './pages/ReportPage';
import { ReportsPage } from './pages/ReportsPage';
import { NotFoundPage } from './pages/NotFoundPage';
import { SettingsPage } from './pages/SettingsPage';
import { ExperimentPage } from './pages/ExperimentPage';

import { ENV } from './services/Environment';

export const Router = () => (
  <BrowserRouter>
    <AuthProvider>
      <Routes>
        <Route path={ENV.HOME_PATH} >
          <Route index element={
            <RequireAuth>
              <HomePage />
            </RequireAuth>
          } />

          <Route path="*" element={<NotFoundPage />} />

          <Route path={ENV.LOGIN_PATH.replace('/', '')} element={<LoginPage />} />

          <Route path={ENV.REPORTS_PATH.replace('/', '')} >
            <Route index element={
              <RequireAuth>
                <ReportsPage />
              </RequireAuth>
            } />
            <Route path=":reportId" element={
              <RequireAuth>
                <ReportPage />
              </RequireAuth>
            } />
          </Route>

          <Route path={`${ENV.EXPERIMENT_PATH.replace('/', '')}/:moduleId`} element={
            <RequireAuth>
              <ExperimentPage />
            </RequireAuth>
          } />
          <Route path={ENV.SETTINGS_PATH.replace('/', '')} element={
            <RequireAuth>
              <SettingsPage />
            </RequireAuth>
          } />
          <Route path={`${ENV.MODULE_PATH.replace('/', '')}/:moduleId`} element={
            <RequireAuth>
              <InterfacePage />
            </RequireAuth>
          } />
          <Route path={ENV.ABOUT_PATH.replace('/', '')} element={
            <RequireAuth>
              <AboutPage />
            </RequireAuth>
          } />
        </Route>
      </Routes>
    </AuthProvider>
  </BrowserRouter>
)
