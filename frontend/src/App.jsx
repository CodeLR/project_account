import { useState } from 'react'
import {
  PlasmicComponent,
  PlasmicRootProvider,
} from '@plasmicapp/loader-react'
import { PLASMIC } from './plasmic-init'

function App() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [profile, setProfile] = useState(null)
  const [refreshToken, setRefreshToken] = useState(null)
  async function handleLogin() {
    try {
      console.log('Email:', email)
      console.log('Password length:', password.length)
      const response = await fetch('http://127.0.0.1:8000/auth/login',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: email,
            password: password,
          }),
        })

      const data = await response.json()
      if (response.ok) {
        const accessToken = data.access_token
        setRefreshToken(data.refresh_token)

        const profileResponse = await fetch(
          'http://127.0.0.1:8000/user/me',
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${accessToken}`,
            },
          }
        )

        const userProfile = await profileResponse.json()

        setProfile(userProfile)

        console.log('Профиль пользователя:', userProfile)
      }

      console.log('Ответ FastAPI:', data)

    } catch (error) {
      console.error('Ошибка подключения:', error)
    }
  }
  async function handleLogout() {
    try {
      const response = await fetch(
        'http://127.0.0.1:8000/auth/logout',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            refresh_token: refreshToken,
          }),
        }
      )

      if (response.ok) {
        setProfile(null)
        setRefreshToken(null)
        setPassword('')
        setEmail('')
        console.log('Вы успешно вышли из аккаунта')
      } else {
        console.error('Не удалось выйти из аккаунта')
      }
    } catch (error) {
      console.error('Ошибка при выходе:', error)
    }
  }

  return (
    <PlasmicRootProvider loader={PLASMIC}>
      {profile ? (
        <div style={{
          maxWidth: '600px',
          margin: '50px auto',
          fontFamily: 'Arial',
          padding: '20px'
        }}>
          <h1>Привет, {profile.name}! 👋</h1>

          <h2>Информация о пользователе</h2>

          <table style={{
            width: '100%',
            borderCollapse: 'collapse'
          }}>
            <tbody>
              <tr>
                <th style={{ textAlign: 'left', padding: '10px', border: '1px solid #ccc' }}>ID</th>
                <td style={{ padding: '10px', border: '1px solid #ccc' }}>{profile.id}</td>
              </tr>
              <tr>
                <th style={{ textAlign: 'left', padding: '10px', border: '1px solid #ccc' }}>Имя</th>
                <td style={{ padding: '10px', border: '1px solid #ccc' }}>{profile.name}</td>
              </tr>
              <tr>
                <th style={{ textAlign: 'left', padding: '10px', border: '1px solid #ccc' }}>Email</th>
                <td style={{ padding: '10px', border: '1px solid #ccc' }}>{profile.email}</td>
              </tr>
              <tr>
                <th style={{ textAlign: 'left', padding: '10px', border: '1px solid #ccc' }}>Роль</th>
                <td style={{ padding: '10px', border: '1px solid #ccc' }}>{profile.role}</td>
              </tr>
            </tbody>
          </table>
          <button
            onClick={handleLogout}
            style={{
              marginTop: '20px',
              padding: '10px 24px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '16px'
            }}
          >
            Выйти
          </button>
        </div>
      ) : (
        <PlasmicComponent
          component="Homepage"
          componentProps={{
            email: {
              props: {
                value: email,
                onChange: (event) => setEmail(event.target.value),
              },
            },
            password: {
              props: {
                value: password,
                onChange: (value) => setPassword(
                  typeof value === 'string' ? value : value.target.value
                ),
              },
            },
            button: {
              props: {
                onClick: handleLogin,
              },
            },
          }}
        />
      )}
    </PlasmicRootProvider>
  )

}

export default App